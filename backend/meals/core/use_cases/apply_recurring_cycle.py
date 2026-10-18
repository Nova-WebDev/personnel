from datetime import date, datetime

from meals.core.entities.applied_day import AppliedDay
from meals.core.interfaces.meal_plan_repository import IMealPlanRepository
from meals.core.use_cases.get_meal_plan_time_policies import GetMealPlanTimePolicies
from meals.utility.reservation_deadline import is_deadline_passed


class ApplyRecurringCycle:
    def __init__(
        self,
        meal_plan_repository: IMealPlanRepository,
        get_time_policies: GetMealPlanTimePolicies,
    ):
        self.meal_plan_repository = meal_plan_repository
        self.get_time_policies = get_time_policies

    async def execute(
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
    def serialize_day(day: AppliedDay) -> dict:
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