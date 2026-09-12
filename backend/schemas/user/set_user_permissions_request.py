from pydantic import BaseModel


class PermissionInput(BaseModel):
    level: str
    scope: str | None = None


class SetUserPermissionsRequest(BaseModel):
    permissions: list[PermissionInput]