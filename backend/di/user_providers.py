from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher

from user.core.use_cases.create_branch import CreateBranch
from user.core.use_cases.update_branch import UpdateBranch
from user.core.use_cases.create_unit import CreateUnit
from user.core.use_cases.update_unit import UpdateUnit
from user.core.use_cases.delete_branch import DeleteBranch
from user.core.use_cases.delete_unit import DeleteUnit
from user.core.use_cases.get_branches_with_units import GetBranchesWithUnits
from user.core.use_cases.get_users_with_location import GetUsersWithLocation
from user.core.use_cases.create_user import CreateUser

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

def get_update_unit_uc(session: AsyncSession) -> UpdateUnit:
    return UpdateUnit(
        unit_repository=UnitRepository(session),
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_delete_branch_uc(session: AsyncSession) -> DeleteBranch:
    return DeleteBranch(
        branch_repository=BranchRepository(session),
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_delete_unit_uc(session: AsyncSession) -> DeleteUnit:
    return DeleteUnit(
        unit_repository=UnitRepository(session),
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )

def get_branches_with_units_uc(session: AsyncSession) -> GetBranchesWithUnits:
    return GetBranchesWithUnits(
        branch_repository=BranchRepository(session),
    )

def get_users_with_location_uc(session: AsyncSession) -> GetUsersWithLocation:
    return GetUsersWithLocation(
        user_repository=UserRepository(session),
    )

def get_create_user_uc(session: AsyncSession) -> CreateUser:
    return CreateUser(
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
    )