from datetime import datetime
from pydantic import BaseModel


class ScopeInfoResponse(BaseModel):
    level: str
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None


class UserProfileResponse(BaseModel):
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
    scopes: list[ScopeInfoResponse]