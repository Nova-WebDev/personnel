from abc import ABC, abstractmethod
from user.core.entities.unit import Unit


class IUnitRepository(ABC):
    @abstractmethod
    async def create(self, name: str, branch_id: str) -> Unit:
        pass