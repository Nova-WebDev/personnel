import uuid
from dataclasses import dataclass

from personnel.core.entities.position import PersonnelPosition


@dataclass(frozen=True)
class PersonnelDetailEntity:
    uuid: uuid.UUID
    personnel_id: str
    first_name: str
    last_name: str
    photo_path: str | None
    position: PersonnelPosition | None
    is_blocked: bool
    branch_name: str | None
    unit_name: str | None