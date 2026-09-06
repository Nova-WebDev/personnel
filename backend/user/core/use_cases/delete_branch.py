from user.core.interfaces.branch_repository import IBranchRepository
from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class DeleteBranch:
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

    async def execute(self, branch_id: str, permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()

        member_ids = await self.user_repository.get_user_ids_by_branch(branch_id)
        permission_ids = await self.permission_repository.get_global_and_branch_scoped_user_ids(branch_id)
        targets = list(set(member_ids) | set(permission_ids))

        await self.branch_repository.delete(branch_id)

        await self.event_publisher.publish(
            event="branch.deleted",
            scope="branch",
            data={"id": branch_id},
            targets=targets,
        )