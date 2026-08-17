from pydantic import BaseModel


class BranchResponse(BaseModel):
    id: int
    name: str