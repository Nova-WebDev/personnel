from dataclasses import dataclass
from datetime import date


@dataclass
class ReservationContext:
    plan_date: date
    meal_is_active: bool
    user_is_blocked: bool
    user_unit_id: str | None
    current_voucher_id: str | None
    current_meal_plan_id: str | None
    current_is_used: bool | None