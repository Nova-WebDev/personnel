from datetime import date, datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from meals.core.entities.applied_day import AppliedDay
from meals.core.errors.meals_errors import (
    InvalidRecurringCycleError,
    MealNotFoundError,
    PermissionDeniedError,
)
from meals.core.interfaces.meal_plan_recurring_repository import IMealPlanRecurringRepository
from meals.core.interfaces.meal_plan_repository import IMealPlanRepository
from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.recurring_cycle import advance, is_contiguous
from meals.utility.reservation_deadline import is_deadline_passed
from user.core.entities.permission_level import PermissionLevel
from user.core.interfaces.permission_repository import IPermissionRepository


class SetMealPlanRecurring:
    def __init__(
        self,
        recurring_repository: IMealPlanRecurringRepository,
        meal_plan_repository: IMealPlanRepository,
        meal_repository: IMealRepository,
        permission_repository: IPermissionRepository,
        get_time_policies: GetMealPlanTimePolicies,
        event_publisher: IEventPublisher,
    ):
        self.recurring_repository = recurring_repository
        self.meal_plan_repository = meal_plan_repository
        self.meal_repository = meal_repository
        self.permission_repository = permission_repository
        self.get_time_policies = get_time_policies
        self.event_publisher = event_publisher

    async def execute(self, items: list[dict], permissions: list[dict]) -> None:
        self._authorize(permissions)

        now = datetime.now(timezone.utc)
        items = sorted(items, key=lambda i: i["target_date"])
        self._validate_shape(items, now.date())

        meal_ids = list({i["meal_id"] for i in items if i["meal_id"] is not None})
        statuses = await self.meal_repository.get_active_statuses(meal_ids)
        self._validate_meals_exist(meal_ids, statuses)

        result = advance(items, now.date())
        applied = await self._apply(result.visited, statuses, now)
        cycle = await self.recurring_repository.replace_all(result.rotated)

        if applied:
            await self.event_publisher.publish(
                event="meal_plan.recurring_applied",
                scope="meal_plan",
                data={"days": [self._serialize_day(day) for day in applied]},
                targets=["*"],
            )

        admin_ids = await self.permission_repository.get_admin_user_ids()
        await self.event_publisher.publish(
            event="meal_plan.recurring_cycle_updated",
            scope="meal_plan",
            data={
                "cycle": [
                    {"target_date": c.target_date.isoformat(), "meal_id": c.meal_id}
                    for c in cycle
                ],
            },
            targets=admin_ids,
        )

    async def _apply(
        self,
        visited: list[tuple[date, str | None]],
        statuses: dict[str, bool],
        now: datetime,
    ) -> list[AppliedDay]:
        if not visited:
            return []

        policies = await self.get_time_policies.execute()
        existing = await self.meal_plan_repository.get_by_dates([d for d, _ in visited])

        existing_by_date: dict[date, list] = {}
        for plan in existing:
            existing_by_date.setdefault(plan.plan_date, []).append(plan)

        changes: dict[date, str] = {}
        for day, meal_id in visited:
            if is_deadline_passed(day, policies, now):
                continue

            if meal_id is None or not statuses.get(meal_id, False):
                continue

            if any(p.meal.id == meal_id for p in existing_by_date.get(day, [])):
                continue

            changes[day] = meal_id

        if not changes:
            return []

        await self.meal_plan_repository.replace_days(changes)
        refreshed = await self.meal_plan_repository.get_by_dates(list(changes))

        by_date: dict[date, list] = {}
        for plan in refreshed:
            by_date.setdefault(plan.plan_date, []).append(plan)

        return [AppliedDay(plan_date=d, plans=by_date.get(d, [])) for d in sorted(changes)]

    @staticmethod
    def _serialize_day(day: AppliedDay) -> dict:
        return {
            "plan_date": day.plan_date.isoformat(),
            "plans": [
                {
                    "id": p.id,
                    "meal": {
                        "id": p.meal.id,
                        "title": p.meal.title,
                        "description": p.meal.description,
                        "photo_path": p.meal.photo_path,
                        "is_active": p.meal.is_active,
                    },
                }
                for p in day.plans
            ],
        }

    @staticmethod
    def _validate_shape(items: list[dict], today: date) -> None:
        if not items:
            return

        dates = [i["target_date"] for i in items]

        if len(set(dates)) != len(dates):
            raise InvalidRecurringCycleError("Duplicate dates in cycle")

        if not is_contiguous(dates):
            raise InvalidRecurringCycleError("Cycle dates must be consecutive; use null meal_id for empty days")

        if dates[0] < today:
            raise InvalidRecurringCycleError("Cycle start date cannot be in the past")

    @staticmethod
    def _validate_meals_exist(meal_ids: list[str], statuses: dict[str, bool]) -> None:
        if len(statuses) != len(meal_ids):
            raise MealNotFoundError()

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()