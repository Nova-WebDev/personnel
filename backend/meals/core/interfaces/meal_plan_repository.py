from abc import ABC, abstractmethod
from datetime import date

from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal


class IMealPlanRepository(ABC):
    @abstractmethod
    async def create_for_active_meal(self, plan_date: date, meal_id: str) -> MealPlanWithMeal:
        pass