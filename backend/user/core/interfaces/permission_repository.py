from abc import ABC, abstractmethod
from user.core.entities.user_profile import ScopeInfo

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