from dataclasses import dataclass
from datetime import date, datetime

from meals.core.entities.meal import Meal


@dataclass
class RedeemUser:
    id: str
    phone: str
    first_name: str
    last_name: str
    personnel_code: str | None
    rfid_card_id: str | None
    photo_path: str | None
    is_blocked: bool
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None


@dataclass
class RedeemVoucher:
    id: str
    meal_plan_id: str
    plan_date: date
    meal: Meal
    is_used: bool
    redeemed_at: datetime | None


@dataclass
class RedeemContext:
    user: RedeemUser
    voucher: RedeemVoucher | None