from pydantic import BaseModel


class UnitResponse(BaseModel):
    unit_id: str
    unit_name: str


class BranchWithUnitsResponse(BaseModel):
    branch_id: str
    branch_name: str
    units: list[UnitResponse]