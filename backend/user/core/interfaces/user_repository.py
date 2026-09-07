from abc import ABC, abstractmethod
from user.core.entities.user_with_location import UserWithLocation


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_ids_by_branch(self, branch_id: str) -> list[str]:
        pass

    @abstractmethod
    async def get_user_ids_by_unit(self, unit_id: str) -> list[str]:
        pass

    @abstractmethod
    async def get_all_with_location(self) -> list[UserWithLocation]:
        pass

    @abstractmethod
    async def get_by_unit_ids_with_location(self, unit_ids: list[str]) -> list[UserWithLocation]:
        pass

    @abstractmethod
    async def create(
            self,
            user_id: str,
            phone: str,
            first_name: str,
            last_name: str,
            unit_id: str,
            personnel_code: str | None,
            photo_path: str | None,
    ) -> UserWithLocation:
        pass