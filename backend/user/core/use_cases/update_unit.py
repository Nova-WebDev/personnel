from user.core.interfaces.unit_repository import IUnitRepository
from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class UpdateUnit:
    def __init__(
        self,
        unit_repository: IUnitRepository,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.unit_repository = unit_repository
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, unit_id: str, name: str, permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()

        unit = await self.unit_repository.update(unit_id, name)

        member_ids = await self.user_repository.get_user_ids_by_unit(unit.id)
        permission_ids = await self.permission_repository.get_global_and_unit_scoped_user_ids(unit.id)

        targets = list(set(member_ids) | set(permission_ids))

        await self.event_publisher.publish(
            event="unit.updated",
            scope="unit",
            data={"id": unit.id, "name": unit.name, "branch_id": unit.branch_id},
            targets=targets,
        )