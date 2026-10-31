from datetime import date, datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import (
    MealPlanDeadlinePassedError,
    PermissionDeniedError,
)
from meals.core.interfaces.meal_plan_repository import IMealPlanRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.reservation_deadline import resolve_deadline_utc, weekday_of
from user.core.entities.permission_level import PermissionLevel


class DeleteMealPlan:
    def __init__(
        self,
        meal_plan_repository: IMealPlanRepository,
        get_time_policies: GetMealPlanTimePolicies,
        event_publisher: IEventPublisher,
    ):
        self.meal_plan_repository = meal_plan_repository
        self.get_time_policies = get_time_policies
        self.event_publisher = event_publisher

    async def execute(self, meal_plan_id: str, permissions: list[dict]) -> None:
        self._authorize(permissions)

        plan_date = await self.meal_plan_repository.get_plan_date(meal_plan_id)
        await self._ensure_deadline_not_passed(plan_date)

        await self.meal_plan_repository.delete(meal_plan_id)

        await self.event_publisher.publish(
            event="meal_plan.deleted",
            scope="meal_plan",
            data={"id": meal_plan_id, "plan_date": plan_date.isoformat()},
            targets=["*"],
        )

    async def _ensure_deadline_not_passed(self, plan_date: date) -> None:
        policies = await self.get_time_policies.execute()
        weekday = weekday_of(plan_date)
        policy = next((p for p in policies if p.target_weekday == weekday), None)

        cutoff_before = policy.cutoff_before if policy is not None else 0
        deadline = resolve_deadline_utc(plan_date, cutoff_before)

        if datetime.now(timezone.utc) >= deadline:
            raise MealPlanDeadlinePassedError()

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_kitchen = any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions)

        if not (is_admin or is_kitchen):
            raise PermissionDeniedError()