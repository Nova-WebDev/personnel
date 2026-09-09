from pydantic import BaseModel


class PermissionLevelResponse(BaseModel):
    level: str
    requires_scope: bool