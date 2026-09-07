from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserWithLocation:
    id: str
    phone: str
    first_name: str
    last_name: str
    personnel_code: str | None
    rfid_card_id: str | None
    photo_path: str | None
    is_blocked: bool
    created_at: datetime
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None