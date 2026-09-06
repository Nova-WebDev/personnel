from pydantic import BaseModel


class UpdateBranchRequest(BaseModel):
    name: str