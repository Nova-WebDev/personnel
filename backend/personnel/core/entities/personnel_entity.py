import uuid
from dataclasses import dataclass

from personnel.core.entities.position import PersonnelPosition


@dataclass(frozen=True)
class PersonnelEntity:
    uuid: uuid.UUID
    personnel_id: str
    first_name: str
    last_name: str
    branch_id: int
    unit_id: int | None
    photo_path: str | None
    position: PersonnelPosition | None
    is_blocked: bool