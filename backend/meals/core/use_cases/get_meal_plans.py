from datetime import date

from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal
from meals.core.errors.meals_errors import InvalidDateRangeError
from meals.core.interfaces.meal_plan_repository import IMealPlanRepository

MAX_RANGE_DAYS = 31


class GetMealPlans:
    def __init__(self, meal_plan_repository: IMealPlanRepository):
        self.meal_plan_repository = meal_plan_repository

    async def execute(self, date_from: date, date_to: date) -> list[MealPlanWithMeal]:
        self._validate_range(date_from, date_to)
        return await self.meal_plan_repository.get_by_date_range(date_from, date_to)

    @staticmethod
    def _validate_range(date_from: date, date_to: date) -> None:
        if date_from > date_to or (date_to - date_from).days >= MAX_RANGE_DAYS:
            raise InvalidDateRangeError()