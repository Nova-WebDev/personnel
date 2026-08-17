from pydantic import BaseModel


class UnitResponse(BaseModel):
    id: int
    name: str
    branch_id: int