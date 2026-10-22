import asyncio
from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import (
    InvalidBulkReservationError,
    MealNotActiveError,
    PermissionDeniedError,
    ReservationDeadlinePassedError,
    UserOutOfScopeError,
)
from meals.core.interfaces.voucher_repository import IVoucherRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.reservation_deadline import is_deadline_passed
from user.core.entities.permission_level import PermissionLevel
from user.core.interfaces.permission_repository import IPermissionRepository

MAX_ITEMS = 200


class BulkReserveMeal:
    def __init__(
        self,
        voucher_repository: IVoucherRepository,
        permission_repository: IPermissionRepository,
        get_time_policies: GetMealPlanTimePolicies,
        event_publisher: IEventPublisher,
    ):
        self.voucher_repository = voucher_repository
        self.permission_repository = permission_repository
        self.get_time_policies = get_time_policies
        self.event_publisher = event_publisher

    async def execute(self, meal_plan_id: str, items: list[dict], permissions: list[dict]) -> dict:
        managed_units = self._managed_units(permissions)
        self._validate_items(items)

        user_ids = [item["user_id"] for item in items]
        context = await self.voucher_repository.get_bulk_context(meal_plan_id, user_ids)

        if not context.meal_is_active:
            raise MealNotActiveError()

        policies = await self.get_time_policies.execute()
        if is_deadline_passed(context.plan_date, policies, datetime.now(timezone.utc)):
            raise ReservationDeadlinePassedError()

        self._validate_scope(user_ids, context.users, managed_units)

        to_reserve: dict[str, str | None] = {}
        to_cancel: list[str] = []

        for item in items:
            user_id = item["user_id"]
            existing = context.vouchers.get(user_id)

            if item["reserve"]:
                if context.users[user_id].is_blocked:
                    continue
                if existing is None:
                    to_reserve[user_id] = None
                elif existing.meal_plan_id == meal_plan_id or existing.is_used:
                    continue
                else:
                    to_reserve[user_id] = existing.meal_plan_id
            elif existing is not None and existing.meal_plan_id == meal_plan_id and not existing.is_used:
                to_cancel.append(user_id)

        reserved = await self.voucher_repository.bulk_reserve(meal_plan_id, context.plan_date, list(to_reserve))
        cancelled = await self.voucher_repository.bulk_cancel(meal_plan_id, to_cancel)

        if reserved or cancelled:
            await self._publish(meal_plan_id, context, to_reserve, reserved, cancelled)

        return {"reserved": len(reserved), "cancelled": len(cancelled)}

    async def _publish(self, meal_plan_id, context, previous_plans, reserved, cancelled) -> None:
        affected = set(reserved) | cancelled
        unit_ids = list({context.users[user_id].unit_id for user_id in affected})
        recipients = await self.permission_repository.get_reservation_event_recipients(unit_ids)
        date_text = context.plan_date.isoformat()

        publishes = []

        for user_id, voucher_id in reserved.items():
            targets = recipients.for_unit(context.users[user_id].unit_id, user_id)
            previous_plan_id = previous_plans[user_id]

            if previous_plan_id is not None:
                publishes.append(
                    self.event_publisher.publish(
                        event="voucher.cancelled",
                        scope="voucher",
                        data={"user_id": user_id, "meal_plan_id": previous_plan_id, "reservation_date": date_text},
                        targets=targets,
                    )
                )

            publishes.append(
                self.event_publisher.publish(
                    event="voucher.reserved",
                    scope="voucher",
                    data={
                        "id": voucher_id,
                        "user_id": user_id,
                        "meal_plan_id": meal_plan_id,
                        "reservation_date": date_text,
                    },
                    targets=targets,
                )
            )

        for user_id in cancelled:
            publishes.append(
                self.event_publisher.publish(
                    event="voucher.cancelled",
                    scope="voucher",
                    data={"user_id": user_id, "meal_plan_id": meal_plan_id, "reservation_date": date_text},
                    targets=recipients.for_unit(context.users[user_id].unit_id, user_id),
                )
            )

        await asyncio.gather(*publishes)

    @staticmethod
    def _managed_units(permissions: list[dict]) -> set[str]:
        units = {
            p["scope"]
            for p in permissions
            if p["level"] == PermissionLevel.GROUP_MANAGER.value and p["scope"] is not None
        }

        if not units:
            raise PermissionDeniedError("Group manager permission required")

        return units

    @staticmethod
    def _validate_items(items: list[dict]) -> None:
        if not items or len(items) > MAX_ITEMS:
            raise InvalidBulkReservationError(f"Items must contain between 1 and {MAX_ITEMS} entries")

        user_ids = [item["user_id"] for item in items]
        if len(set(user_ids)) != len(user_ids):
            raise InvalidBulkReservationError("Duplicate users in request")

    @staticmethod
    def _validate_scope(user_ids: list[str], users: dict, managed_units: set[str]) -> None:
        for user_id in user_ids:
            user = users.get(user_id)

            if user is None or user.unit_id not in managed_units:
                raise UserOutOfScopeError()