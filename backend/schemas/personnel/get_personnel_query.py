from pydantic import BaseModel

from personnel.core.entities.personnel_order_by import PersonnelOrderBy


class GetPersonnelQuery(BaseModel):
    page: int = 1
    limit: int = 20
    search: str | None = None
    order_by: PersonnelOrderBy = PersonnelOrderBy.CREATED_AT
    descending: bool = True