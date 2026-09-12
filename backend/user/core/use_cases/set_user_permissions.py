from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from auth.core.interfaces.auth_store import IAuthStore
from user.core.errors.user_errors import PermissionDeniedError, InvalidPermissionScopeError
from user.core.entities.permission_level import PermissionLevel, SCOPED_PERMISSION_LEVELS


class SetUserPermissions:
    def __init__(
        self,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
        auth_store: IAuthStore,
    ):
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher
        self.auth_store = auth_store

    async def execute(self, user_id: str, new_permissions: list[dict], permissions: list[dict]) -> None:
        self._authorize(permissions)
        self._validate_scopes(new_permissions)

        await self.permission_repository.replace_all_for_user(user_id, new_permissions)
        await self.auth_store.update_permissions(user_id, new_permissions)

        admin_ids = await self.permission_repository.get_admin_user_ids()
        targets = list(set(admin_ids) | {user_id})

        await self.event_publisher.publish(
            event="user.permissions_updated",
            scope="permission",
            data={"user_id": user_id, "permissions": new_permissions},
            targets=targets,
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)

        if not is_admin:
            raise PermissionDeniedError()

    @staticmethod
    def _validate_scopes(new_permissions: list[dict]) -> None:
        for p in new_permissions:
            level = PermissionLevel(p["level"])
            scope = p.get("scope")

            requires_scope = level in SCOPED_PERMISSION_LEVELS

            if requires_scope and scope is None:
                raise InvalidPermissionScopeError()
            if not requires_scope and scope is not None:
                raise InvalidPermissionScopeError()