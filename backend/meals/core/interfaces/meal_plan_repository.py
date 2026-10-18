from abc import ABC, abstractmethod
from datetime import date

from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal


class IMealPlanRepository(ABC):
    @abstractmethod
    async def create_for_active_meal(self, plan_date: date, meal_id: str) -> MealPlanWithMeal:
        pass

    @abstractmethod
    async def get_plan_date(self, meal_plan_id: str) -> date:
        pass

    @abstractmethod
    async def change_meal(self, meal_plan_id: str, meal_id: str) -> MealPlanWithMeal:
        pass

    @abstractmethod
    async def delete(self, meal_plan_id: str) -> None:
        pass

    @abstractmethod
    async def get_by_date_range(self, date_from: date, date_to: date) -> list[MealPlanWithMeal]:
        pass