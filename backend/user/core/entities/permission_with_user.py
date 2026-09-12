from dataclasses import dataclass


@dataclass
class PermissionWithUser:
    permission_id: str
    user_id: str
    first_name: str
    last_name: str
    level: str
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None