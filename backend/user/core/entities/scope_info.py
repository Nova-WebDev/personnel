from dataclasses import dataclass


@dataclass
class ScopeInfo:
    level: str
    unit_id: str | None
    unit_name: str | None
    branch_id: str | None
    branch_name: str | None