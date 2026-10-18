from dataclasses import dataclass
from datetime import date


@dataclass
class MealPlanRecurring:
    id: str
    target_date: date
    meal_id: str | None