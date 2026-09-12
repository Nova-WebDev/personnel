from abc import ABC, abstractmethod
from user.core.entities.user_profile import ScopeInfo
from user.core.entities.permission_with_user import PermissionWithUser

class IPermissionRepository(ABC):
    @abstractmethod
    async def get_admin_user_ids(self) -> list[str]:
        pass

    @abstractmethod
    async def get_global_and_branch_scoped_user_ids(self, branch_id: str) -> list[str]:
        pass

    @abstractmethod
    async def get_global_and_unit_scoped_user_ids(self, unit_id: str) -> list[str]:
        pass

    @abstractmethod
    async def get_scopes_with_location(self, permissions: list[dict]) -> list[ScopeInfo]:
        pass

    @abstractmethod
    async def get_all_with_user_and_location(self) -> list[PermissionWithUser]:
        pass

    @abstractmethod
    async def delete_all_by_user_id(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def replace_all_for_user(self, user_id: str, permissions: list[dict]) -> None:
        pass