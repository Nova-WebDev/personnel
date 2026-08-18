from pydantic import BaseModel

from personnel.core.entities.position import PersonnelPosition


class UpdatePersonnelRequest(BaseModel):
    personnel_id: str
    first_name: str
    last_name: str
    branch_id: int
    unit_id: int | None = None
    position: PersonnelPosition | None = None