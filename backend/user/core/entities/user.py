from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    phone: str
    first_name: str
    last_name: str
    personnel_code: str | None
    rfid_card_id: str | None
    unit_id: str | None
    is_blocked: bool
    created_at: datetime