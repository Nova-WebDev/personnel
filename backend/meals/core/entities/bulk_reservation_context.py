from dataclasses import dataclass
from datetime import date


@dataclass
class BulkUserInfo:
    unit_id: str | None
    is_blocked: bool


@dataclass
class ExistingVoucher:
    meal_plan_id: str
    is_used: bool


@dataclass
class BulkReservationContext:
    plan_date: date
    meal_is_active: bool
    users: dict[str, BulkUserInfo]
    vouchers: dict[str, ExistingVoucher]