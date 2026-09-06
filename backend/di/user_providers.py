from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher

from user.core.use_cases.create_branch import CreateBranch
from user.core.use_cases.update_branch import UpdateBranch
from user.core.use_cases.create_unit import CreateUnit

from user.infrastructure.data.repositories.branch_repository import BranchRepository
from user.infrastructure.data.repositories.permission_repository import PermissionRepository
from user.infrastructure.data.repositories.user_repository import UserRepository
from user.infrastructure.data.repositories.unit_repository import UnitRepository



def get_create_branch_uc(session: AsyncSession) -> CreateBranch:
    return CreateBranch(
        branch_repository=BranchRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_update_branch_uc(session: AsyncSession) -> UpdateBranch:
    return UpdateBranch(
        branch_repository=BranchRepository(session),
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_create_unit_uc(session: AsyncSession) -> CreateUnit:
    return CreateUnit(
        unit_repository=UnitRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )