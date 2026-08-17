from pydantic import BaseModel


class CreateUnitRequest(BaseModel):
    name: str
    branch_id: int