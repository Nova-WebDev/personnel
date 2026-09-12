from user.core.interfaces.permission_repository import IPermissionRepository
from user.core.entities.permission_with_user import PermissionWithUser
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class GetAllPermissions:
    def __init__(self, permission_repository: IPermissionRepository):
        self.permission_repository = permission_repository

    async def execute(self, permissions: list[dict]) -> list[PermissionWithUser]:
        self._authorize(permissions)
        return await self.permission_repository.get_all_with_user_and_location()

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)

        if not is_admin:
            raise PermissionDeniedError()