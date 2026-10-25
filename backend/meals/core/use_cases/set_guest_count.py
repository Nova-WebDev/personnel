from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import (
    InvalidGuestCountError,
    MealNotActiveError,
    PermissionDeniedError,
    ReservationDeadlinePassedError,
)
from meals.core.interfaces.guest_repository import IGuestRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.reservation_deadline import is_deadline_passed
from user.core.entities.permission_level import PermissionLevel
from user.core.interfaces.permission_repository import IPermissionRepository

MAX_GUESTS = 50


class SetGuestCount:
    def __init__(
        self,
        guest_repository: IGuestRepository,
        permission_repository: IPermissionRepository,
        get_time_policies: GetMealPlanTimePolicies,
        event_publisher: IEventPublisher,
    ):
        self.guest_repository = guest_repository
        self.permission_repository = permission_repository
        self.get_time_policies = get_time_policies
        self.event_publisher = event_publisher

    async def execute(
        self, meal_plan_id: str, unit_id: str, guest_count: int, user_id: str, permissions: list[dict]
    ) -> int:
        self._authorize(unit_id, permissions)

        if not 0 <= guest_count <= MAX_GUESTS:
            raise InvalidGuestCountError()

        plan_date, meal_is_active = await self.guest_repository.get_plan_context(meal_plan_id)

        if not meal_is_active:
            raise MealNotActiveError()

        policies = await self.get_time_policies.execute()
        if is_deadline_passed(plan_date, policies, datetime.now(timezone.utc)):
            raise ReservationDeadlinePassedError()

        unit_total = await self.guest_repository.set_guest_count(
            meal_plan_id, unit_id, user_id, plan_date, guest_count
        )

        recipients = await self.permission_repository.get_reservation_event_recipients([unit_id])

        await self.event_publisher.publish(
            event="guest.updated",
            scope="guest",
            data={
                "meal_plan_id": meal_plan_id,
                "unit_id": unit_id,
                "reservation_date": plan_date.isoformat(),
                "total": unit_total,
            },
            targets=recipients.for_unit(unit_id, user_id),
        )

        return guest_count

    @staticmethod
    def _authorize(unit_id: str, permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_manager = any(
            p["level"] == PermissionLevel.GROUP_MANAGER.value and p["scope"] == unit_id for p in permissions
        )

        if not (is_admin or is_manager):
            raise PermissionDeniedError()