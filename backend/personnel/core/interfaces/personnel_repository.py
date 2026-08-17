from abc import ABC, abstractmethod
from personnel.core.entities.branch_entity import BranchEntity


class IPersonnelRepository(ABC):
    @abstractmethod
    async def create_branch(self, name: str) -> BranchEntity:
        pass
