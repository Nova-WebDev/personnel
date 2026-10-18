from dataclasses import dataclass
from datetime import date

from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal


@dataclass
class AppliedDay:
    plan_date: date
    plans: list[MealPlanWithMeal]