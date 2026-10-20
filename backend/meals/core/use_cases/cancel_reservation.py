from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import (
    ReservationDeadlinePassedError,
    VoucherAlreadyUsedError,
    VoucherNotFoundError,
)
from meals.core.interfaces.voucher_repository import IVoucherRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.reservation_deadline import is_deadline_passed
from user.core.interfaces.permission_repository import IPermissionRepository


class CancelReservation:
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

    async def execute(self, user_id: str, meal_plan_id: str) -> None:
        context = await self.voucher_repository.get_cancellation_context(user_id, meal_plan_id)

        policies = await self.get_time_policies.execute()
        if is_deadline_passed(context.plan_date, policies, datetime.now(timezone.utc)):
            raise ReservationDeadlinePassedError()

        if not await self.voucher_repository.delete_unused(user_id, meal_plan_id):
            await self._raise_failure_reason(user_id, meal_plan_id)

        targets = await self.permission_repository.get_reservation_event_user_ids(context.user_unit_id)
        targets = list(set(targets) | {user_id})

        await self.event_publisher.publish(
            event="voucher.cancelled",
            scope="voucher",
            data={
                "user_id": user_id,
                "meal_plan_id": meal_plan_id,
                "reservation_date": context.plan_date.isoformat(),
            },
            targets=targets,
        )

    async def _raise_failure_reason(self, user_id: str, meal_plan_id: str) -> None:
        is_used = await self.voucher_repository.is_used(user_id, meal_plan_id)

        if is_used:
            raise VoucherAlreadyUsedError()

        raise VoucherNotFoundError()