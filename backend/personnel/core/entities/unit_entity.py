from dataclasses import dataclass


@dataclass(frozen=True)
class UnitEntity:
    id: int
    name: str
    branch_id: int