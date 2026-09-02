from dataclasses import dataclass
from datetime import date

@dataclass
class MealPlanRecurring:
    id: str
    meal_id: str | None
    target_date: date
    order_index: int