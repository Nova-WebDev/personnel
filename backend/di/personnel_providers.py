from sqlalchemy.ext.asyncio import AsyncSession

from personnel.infrastructure.data.personnel_repository import PersonnelRepository

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
    return CreatePersonnel(repo)


def get_update_personnel_uc(session: AsyncSession) -> UpdatePersonnel:
    repo = PersonnelRepository(session)
    return UpdatePersonnel(repo)


def get_set_personnel_block_status_uc(session: AsyncSession) -> SetPersonnelBlockStatus:
    repo = PersonnelRepository(session)
    return SetPersonnelBlockStatus(repo)