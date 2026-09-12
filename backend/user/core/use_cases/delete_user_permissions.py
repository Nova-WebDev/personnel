from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from auth.core.interfaces.auth_store import IAuthStore
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class DeleteUserPermissions:
    def __init__(
        self,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
        auth_store: IAuthStore,
    ):
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher
        self.auth_store = auth_store

    async def execute(self, user_id: str, permissions: list[dict]) -> None:
        self._authorize(permissions)

        admin_ids = await self.permission_repository.get_admin_user_ids()

        await self.permission_repository.delete_all_by_user_id(user_id)
        await self.auth_store.update_permissions(user_id, [])

        targets = list(set(admin_ids) | {user_id})

        await self.event_publisher.publish(
            event="user.permissions_deleted",
            scope="permission",
            data={"user_id": user_id},
            targets=targets,
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)

        if not is_admin:
            raise PermissionDeniedError()