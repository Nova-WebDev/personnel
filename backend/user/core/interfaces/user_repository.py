from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_ids_by_branch(self, branch_id: str) -> list[str]:
        pass

    @abstractmethod
    async def get_user_ids_by_unit(self, unit_id: str) -> list[str]:
        pass