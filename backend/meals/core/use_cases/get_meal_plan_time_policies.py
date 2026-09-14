import json

from meals.core.interfaces.meal_plan_time_policy_repository import IMealPlanTimePolicyRepository
from meals.core.interfaces.cache_store import ICacheStore
from meals.core.entities.meal_plan_time_policy import MealPlanTimePolicy
from meals.core.entities.week_day import WeekDay

CACHE_KEY = "meal_plan_time_policies"


class GetMealPlanTimePolicies:
    def __init__(
        self,
        policy_repository: IMealPlanTimePolicyRepository,
        cache_store: ICacheStore,
    ):
        self.policy_repository = policy_repository
        self.cache_store = cache_store

    async def execute(self) -> list[MealPlanTimePolicy]:
        cached = await self.cache_store.get(CACHE_KEY)

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
        await self.cache_store.set(CACHE_KEY, json.dumps(payload))

        return policies