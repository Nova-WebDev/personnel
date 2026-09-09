from dataclasses import dataclass, field
from datetime import datetime
from user.core.entities.scope_info import ScopeInfo


@dataclass
class UserProfile:
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
    scopes: list[ScopeInfo] = field(default_factory=list)