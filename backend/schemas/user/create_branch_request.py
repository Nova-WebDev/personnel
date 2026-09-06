from pydantic import BaseModel


class CreateBranchRequest(BaseModel):
    name: str