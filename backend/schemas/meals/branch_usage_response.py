from pydantic import BaseModel


class BranchUsageItem(BaseModel):
    branch_id: str
    branch_name: str
    used: int
    unused: int