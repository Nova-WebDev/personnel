from dataclasses import dataclass
from datetime import date


@dataclass
class VoucherSummary:
    id: str
    user_id: str
    meal_plan_id: str
    reservation_date: date