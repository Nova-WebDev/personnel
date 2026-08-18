from dataclasses import dataclass

from personnel.core.entities.unit_entity import UnitEntity


@dataclass(frozen=True)
class BranchWithUnitsEntity:
    id: int
    name: str
    units: list[UnitEntity]