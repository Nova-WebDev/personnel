from dataclasses import dataclass


@dataclass(frozen=True)
class BranchEntity:
    id: int | None
    name: str
