from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class SetUserBlockedStatus:
    def __init__(
        self,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, user_id: str, is_blocked: bool, permissions: list[dict]) -> None:
        current = await self.user_repository.get_by_id(user_id)
        self._authorize(current.unit_id, permissions)

        user = await self.user_repository.set_blocked_status(user_id, is_blocked)

        targets = []
        if user.unit_id is not None:
            targets = await self.permission_repository.get_global_and_unit_scoped_user_ids(user.unit_id)

        targets = list(set(targets) | {user_id})

        await self.event_publisher.publish(
            event="user.blocked_status_changed",
            scope="user",
            data={"id": user.id, "is_blocked": user.is_blocked},
            targets=targets,
        )

    @staticmethod
    def _authorize(unit_id: str | None, permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_hr_for_unit = (
            unit_id is not None
            and any(p["level"] == PermissionLevel.HR_MANAGER.value and p["scope"] == unit_id for p in permissions)
        )

        if not (is_admin or is_hr_for_unit):
            raise PermissionDeniedError()