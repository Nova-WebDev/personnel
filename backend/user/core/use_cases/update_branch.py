from user.core.interfaces.branch_repository import IBranchRepository
from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel

from app.interfaces.event_publisher import IEventPublisher


class UpdateBranch:
    def __init__(
        self,
        branch_repository: IBranchRepository,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
    ):
        self.branch_repository = branch_repository
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher

    async def execute(self, branch_id: str, name: str, permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()

        branch = await self.branch_repository.update(branch_id, name)

        member_ids = await self.user_repository.get_user_ids_by_branch(branch.id)
        permission_ids = await self.permission_repository.get_global_and_branch_scoped_user_ids(branch.id)

        targets = list(set(member_ids) | set(permission_ids))

        await self.event_publisher.publish(
            event="branch.updated",
            scope="branch",
            data={"id": branch.id, "name": branch.name},
            targets=targets,
        )