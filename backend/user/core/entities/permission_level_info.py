from dataclasses import dataclass


@dataclass
class PermissionLevelInfo:
    level: str
    requires_scope: bool