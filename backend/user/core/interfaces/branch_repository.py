from abc import ABC, abstractmethod
from user.core.entities.branch import Branch


class IBranchRepository(ABC):
    @abstractmethod
    async def create(self, name: str) -> Branch:
        pass

    @abstractmethod
    async def update(self, branch_id: str, name: str) -> Branch:
        pass