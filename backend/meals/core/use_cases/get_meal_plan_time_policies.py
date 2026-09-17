import json

from meals.core.interfaces.meal_plan_time_policy_repository import IMealPlanTimePolicyRepository
from meals.core.interfaces.time_policy_cache import ITimePolicyCache
from meals.core.entities.meal_plan_time_policy import MealPlanTimePolicy
from meals.core.entities.week_day import WeekDay


class GetMealPlanTimePolicies:
    def __init__(
        self,
        policy_repository: IMealPlanTimePolicyRepository,
        time_policy_cache: ITimePolicyCache,
    ):
        self.policy_repository = policy_repository
        self.time_policy_cache = time_policy_cache

    async def execute(self) -> list[MealPlanTimePolicy]:
        cached = await self.time_policy_cache.get_all()

        if cached is not None:
            data = json.loads(cached)
            return [
                MealPlanTimePolicy(
                    id=item["id"],
                    target_weekday=WeekDay(item["target_weekday"]),
                    cutoff_hours_before=item["cutoff_hours_before"],
                )
                for item in data
            ]

        policies = await self.policy_repository.get_all()

        payload = [
            {"id": p.id, "target_weekday": p.target_weekday.value, "cutoff_hours_before": p.cutoff_hours_before}
            for p in policies
        ]
        await self.time_policy_cache.set_all(json.dumps(payload))

        return policies