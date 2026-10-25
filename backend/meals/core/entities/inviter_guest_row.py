from dataclasses import dataclass

from meals.core.entities.meal import Meal


@dataclass
class InviterGuestRow:
    meal_plan_id: str
    meal: Meal
    guest_count: int
    is_used: bool