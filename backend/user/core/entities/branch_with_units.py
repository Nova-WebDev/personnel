from dataclasses import dataclass, field
from user.core.entities.unit import Unit


@dataclass
class BranchWithUnits:
    branch_id: str
    branch_name: str
    units: list[Unit] = field(default_factory=list)