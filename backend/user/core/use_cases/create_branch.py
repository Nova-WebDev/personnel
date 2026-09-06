from user.core.interfaces.branch_repository import IBranchRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel

class CreateBranch:
    def __init__(
        self,
        branch_repository: IBranchRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.branch_repository = branch_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, name: str, permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()

        branch = await self.branch_repository.create(name)
        admin_ids = await self.permission_repository.get_admin_user_ids()

        await self.event_publisher.publish(
            event="branch.created",
            scope="branch",
            data={"id": branch.id, "name": branch.name},
            targets=admin_ids,
        )