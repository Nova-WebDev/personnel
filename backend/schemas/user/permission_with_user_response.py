from pydantic import BaseModel


class PermissionWithUserResponse(BaseModel):
    permission_id: str
    user_id: str
    first_name: str
    last_name: str
    level: str
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None