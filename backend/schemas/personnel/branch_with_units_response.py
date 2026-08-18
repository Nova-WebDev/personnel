from pydantic import BaseModel

from schemas.personnel.unit_nested_response import UnitNestedResponse


class BranchWithUnitsResponse(BaseModel):
    id: int
    name: str
    units: list[UnitNestedResponse]