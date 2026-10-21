from dataclasses import dataclass
from datetime import date

from meals.core.entities.meal import Meal


@dataclass
class MealPlanWithMeal:
    id: str
    plan_date: date
    meal: Meal
    is_reserved: bool = False