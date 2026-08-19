from app.settings import settings
from app.redis.redis_client import redis_client

from sqlalchemy.ext.asyncio import AsyncSession

from personnel.infrastructure.data.personnel_repository import PersonnelRepository
from personnel.infrastructure.storage.image_format_validator import ImageFormatValidator
from personnel.infrastructure.storage.local_image_processor import LocalImageProcessor
from personnel.infrastructure.qrcode.qr_code_generator import QRCodeGenerator
from personnel.infrastructure.rate_limit.redis_qr_rate_limiter import RedisQRRateLimiter

from personnel.core.use_cases.create_branch import CreateBranch
from personnel.core.use_cases.create_unit import CreateUnit
from personnel.core.use_cases.update_branch import UpdateBranch
from personnel.core.use_cases.delete_branch import DeleteBranch
from personnel.core.use_cases.update_unit_name import UpdateUnitName
from personnel.core.use_cases.delete_unit import DeleteUnit
from personnel.core.use_cases.get_all_branches_with_units import GetAllBranchesWithUnits
from personnel.core.use_cases.create_personnel import CreatePersonnel
from personnel.core.use_cases.update_personnel import UpdatePersonnel
from personnel.core.use_cases.set_personnel_block_status import SetPersonnelBlockStatus
from personnel.core.use_cases.get_personnel_paginated import GetPersonnelPaginated
from personnel.core.use_cases.get_personnel_photo import GetPersonnelPhoto
from personnel.core.use_cases.get_personnel_qr_code import GetPersonnelQRCode
from personnel.core.use_cases.get_personnel_detail import GetPersonnelDetail


def get_create_branch_uc(session: AsyncSession) -> CreateBranch:
    repo = PersonnelRepository(session)
    return CreateBranch(repo)


def get_create_unit_uc(session: AsyncSession) -> CreateUnit:
    repo = PersonnelRepository(session)
    return CreateUnit(repo)


def get_update_branch_uc(session: AsyncSession) -> UpdateBranch:
    repo = PersonnelRepository(session)
    return UpdateBranch(repo)


def get_delete_branch_uc(session: AsyncSession) -> DeleteBranch:
    repo = PersonnelRepository(session)
    return DeleteBranch(repo)


def get_update_unit_name_uc(session: AsyncSession) -> UpdateUnitName:
    repo = PersonnelRepository(session)
    return UpdateUnitName(repo)


def get_delete_unit_uc(session: AsyncSession) -> DeleteUnit:
    repo = PersonnelRepository(session)
    return DeleteUnit(repo)


def get_all_branches_with_units_uc(session: AsyncSession) -> GetAllBranchesWithUnits:
    repo = PersonnelRepository(session)
    return GetAllBranchesWithUnits(repo)


def get_create_personnel_uc(session: AsyncSession) -> CreatePersonnel:
    repo = PersonnelRepository(session)
    format_validator = ImageFormatValidator()
    image_processor = LocalImageProcessor()
    return CreatePersonnel(repo, format_validator, image_processor)


def get_update_personnel_uc(session: AsyncSession) -> UpdatePersonnel:
    repo = PersonnelRepository(session)
    format_validator = ImageFormatValidator()
    image_processor = LocalImageProcessor()
    return UpdatePersonnel(repo, format_validator, image_processor)


def get_set_personnel_block_status_uc(session: AsyncSession) -> SetPersonnelBlockStatus:
    repo = PersonnelRepository(session)
    return SetPersonnelBlockStatus(repo)

def get_personnel_paginated_uc(session: AsyncSession) -> GetPersonnelPaginated:
    repo = PersonnelRepository(session)
    return GetPersonnelPaginated(repo)

def get_personnel_photo_uc() -> GetPersonnelPhoto:
    image_processor = LocalImageProcessor()
    return GetPersonnelPhoto(image_processor)


def get_personnel_qr_code_uc(session: AsyncSession) -> GetPersonnelQRCode:
    repo = PersonnelRepository(session)
    qr_generator = QRCodeGenerator()
    rate_limiter = RedisQRRateLimiter(redis_client)
    return GetPersonnelQRCode(repo, qr_generator, rate_limiter, domain=settings.frontend_domain)


def get_personnel_detail_uc(session: AsyncSession) -> GetPersonnelDetail:
    repo = PersonnelRepository(session)
    return GetPersonnelDetail(repo)