from abc import ABC, abstractmethod
from meals.core.entities.meal_plan_time_policy import MealPlanTimePolicy


class IMealPlanTimePolicyRepository(ABC):
    @abstractmethod
    async def upsert_all(self, policies: list[dict]) -> list[MealPlanTimePolicy]:
        pass

    @abstractmethod
    async def get_all(self) -> list[MealPlanTimePolicy]:
        pass