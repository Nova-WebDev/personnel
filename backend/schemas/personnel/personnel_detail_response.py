import uuid

from pydantic import BaseModel

from personnel.core.entities.position import PersonnelPosition


class PersonnelDetailResponse(BaseModel):
    uuid: uuid.UUID
    personnel_id: str
    first_name: str
    last_name: str
    photo_path: str | None
    position: PersonnelPosition | None
    is_blocked: bool
    branch_name: str | None
    unit_name: str | None