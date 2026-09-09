from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.events.redis_event_publisher import RedisEventPublisher

from app.images.image_format_validator import ImageFormatValidator
from app.images.local_image_processor import LocalImageProcessor

from auth.infrastructure.store.auth_store import AuthStore

from user.core.use_cases.create_branch import CreateBranch
from user.core.use_cases.update_branch import UpdateBranch
from user.core.use_cases.create_unit import CreateUnit
from user.core.use_cases.update_unit import UpdateUnit
from user.core.use_cases.delete_branch import DeleteBranch
from user.core.use_cases.delete_unit import DeleteUnit
from user.core.use_cases.get_branches_with_units import GetBranchesWithUnits
from user.core.use_cases.get_users_with_location import GetUsersWithLocation
from user.core.use_cases.create_user import CreateUser
from user.core.use_cases.update_user import UpdateUser
from user.core.use_cases.get_profile_photo import GetProfilePhoto
from user.core.use_cases.set_user_blocked_status import SetUserBlockedStatus
from user.core.use_cases.get_user_qr_code import GetUserQrCode
from user.core.use_cases.get_my_profile import GetMyProfile
from user.core.use_cases.get_public_user_profile import GetPublicUserProfile

from user.infrastructure.data.repositories.branch_repository import BranchRepository
from user.infrastructure.data.repositories.permission_repository import PermissionRepository
from user.infrastructure.data.repositories.user_repository import UserRepository
from user.infrastructure.data.repositories.unit_repository import UnitRepository
from user.infrastructure.qr.qr_code_generator import QRCodeGenerator



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
        format_validator=ImageFormatValidator(),
        image_processor=LocalImageProcessor(),
    )

def get_update_user_uc(session: AsyncSession) -> UpdateUser:
    return UpdateUser(
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        format_validator=ImageFormatValidator(),
        image_processor=LocalImageProcessor(),
    )



def get_profile_photo_uc() -> GetProfilePhoto:
    return GetProfilePhoto(
        image_processor=LocalImageProcessor(),
    )

async def get_set_user_blocked_status_uc(session: AsyncSession) -> SetUserBlockedStatus:
    redis = await redis_client.get_client()
    return SetUserBlockedStatus(
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
        event_publisher=RedisEventPublisher(redis_client),
        auth_store=AuthStore(redis),
    )



def get_user_qr_code_uc(session: AsyncSession) -> GetUserQrCode:
    return GetUserQrCode(
        user_repository=UserRepository(session),
        image_processor=LocalImageProcessor(),
        qr_code_generator=QRCodeGenerator(),
    )

def get_my_profile_uc(session: AsyncSession) -> GetMyProfile:
    return GetMyProfile(
        user_repository=UserRepository(session),
        permission_repository=PermissionRepository(session),
    )

def get_public_user_profile_uc(session: AsyncSession) -> GetPublicUserProfile:
    return GetPublicUserProfile(
        user_repository=UserRepository(session),
    )