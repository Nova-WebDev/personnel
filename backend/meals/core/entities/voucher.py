from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Voucher:
    id: str
    user_id: str
    meal_plan_id: str
    reservation_date: date
    is_used: bool
    redeemed_at: datetime | None
    created_at: datetime