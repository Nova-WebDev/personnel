from abc import ABC, abstractmethod
from user.core.entities.branch import Branch
from user.core.entities.branch_with_units import BranchWithUnits


class IBranchRepository(ABC):
    @abstractmethod
    async def create(self, name: str) -> Branch:
        pass

    @abstractmethod
    async def update(self, branch_id: str, name: str) -> Branch:
        pass

    @abstractmethod
    async def delete(self, branch_id: str) -> None:
        pass

    @abstractmethod
    async def get_all_with_units(self) -> list[BranchWithUnits]:
        pass

    @abstractmethod
    async def get_by_unit_ids_with_units(self, unit_ids: list[str]) -> list[BranchWithUnits]:
        pass