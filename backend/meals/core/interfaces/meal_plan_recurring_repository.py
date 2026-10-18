from abc import ABC, abstractmethod

from meals.core.entities.meal_plan_recurring import MealPlanRecurring


class IMealPlanRecurringRepository(ABC):
    @abstractmethod
    async def replace_all(self, items: list[dict]) -> list[MealPlanRecurring]:
        pass

    @abstractmethod
    async def get_all(self) -> list[MealPlanRecurring]:
        pass