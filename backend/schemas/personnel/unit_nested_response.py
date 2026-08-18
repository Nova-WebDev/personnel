from pydantic import BaseModel


class UnitNestedResponse(BaseModel):
    id: int
    name: str