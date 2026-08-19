from pydantic import BaseModel

from schemas.personnel.personnel_response import PersonnelResponse


class PersonnelPaginatedResponse(BaseModel):
    personnel: list[PersonnelResponse]
    total_count: int