import uuid

from pydantic import BaseModel

from personnel.core.entities.position import PersonnelPosition


class PersonnelResponse(BaseModel):
    uuid: uuid.UUID
    personnel_id: str
    first_name: str
    last_name: str
    branch_id: int
    unit_id: int | None
    photo_path: str | None
    position: PersonnelPosition | None
    is_blocked: bool