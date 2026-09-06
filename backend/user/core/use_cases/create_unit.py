from user.core.interfaces.unit_repository import IUnitRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class CreateUnit:
    def __init__(
        self,
        unit_repository: IUnitRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.unit_repository = unit_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, name: str, branch_id: str, permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()

        unit = await self.unit_repository.create(name, branch_id)
        admin_ids = await self.permission_repository.get_admin_user_ids()

        await self.event_publisher.publish(
            event="unit.created",
            scope="unit",
            data={"id": unit.id, "name": unit.name, "branch_id": unit.branch_id},
            targets=admin_ids,
        )