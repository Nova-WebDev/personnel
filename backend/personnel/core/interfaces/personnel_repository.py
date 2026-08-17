from abc import ABC, abstractmethod

from personnel.core.entities.branch_entity import BranchEntity
from personnel.core.entities.unit_entity import UnitEntity


class IPersonnelRepository(ABC):
    @abstractmethod
    async def create_branch(self, name: str) -> BranchEntity:
        pass

    @abstractmethod
    async def create_unit(self, name: str, branch_id: int) -> UnitEntity:
        pass

    @abstractmethod
    async def update_branch(self, branch_id: int, name: str) -> BranchEntity:
        pass

    @abstractmethod
    async def delete_branch(self, branch_id: int) -> None:
        pass

    @abstractmethod
    async def update_unit_name(self, unit_id: int, name: str) -> None:
        pass

    @abstractmethod
    async def delete_unit(self, unit_id: int) -> None:
        pass