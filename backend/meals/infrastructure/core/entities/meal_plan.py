from dataclasses import dataclass
from datetime import date

@dataclass
class MealPlan:
    id: str
    plan_date: date
    meal_id: str