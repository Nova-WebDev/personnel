
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.branch_entity import BranchEntity
from personnel.core.entities.unit_entity import UnitEntity
from personnel.core.errors.personnel_errors import (
    BranchAlreadyExistsError,
    BranchNotFoundError,
    UnitAlreadyExistsError,
    UnitNotFoundError,
)
from personnel.infrastructure.data.models import Branch, Unit


class PersonnelRepository(IPersonnelRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_branch(self, name: str) -> BranchEntity:
        branch = Branch(name=name)
        self.session.add(branch)

        try:
            await self.session.flush()
        except IntegrityError:
            raise BranchAlreadyExistsError()

        await self.session.refresh(branch)

        return BranchEntity(
            id=branch.id,
            name=branch.name,
        )

    async def create_unit(self, name: str, branch_id: int) -> UnitEntity:
        unit = Unit(name=name, branch_id=branch_id)
        self.session.add(unit)

        try:
            await self.session.flush()
        except IntegrityError as e:
            error_message = str(e.orig) if e.orig else ""
            if "uq_unit_name_branch_id" in error_message:
                raise UnitAlreadyExistsError()
            raise BranchNotFoundError()

        await self.session.refresh(unit)

        return UnitEntity(
            id=unit.id,
            name=unit.name,
            branch_id=unit.branch_id,
        )

    async def update_branch(self, branch_id: int, name: str) -> BranchEntity:
        stmt = select(Branch).where(Branch.id == branch_id)
        result = await self.session.execute(stmt)
        branch = result.scalar_one_or_none()

        if branch is None:
            raise BranchNotFoundError()

        branch.name = name

        try:
            await self.session.flush()
        except IntegrityError:
            raise BranchAlreadyExistsError()

        return BranchEntity(id=branch_id, name=name)

    async def delete_branch(self, branch_id: int) -> None:
        stmt = select(Branch).where(Branch.id == branch_id)
        result = await self.session.execute(stmt)
        branch = result.scalar_one_or_none()

        if branch is None:
            raise BranchNotFoundError()

        await self.session.delete(branch)
        await self.session.flush()

    async def update_unit_name(self, unit_id: int, name: str) -> None:
        stmt = select(Unit).where(Unit.id == unit_id)
        result = await self.session.execute(stmt)
        unit = result.scalar_one_or_none()

        if unit is None:
            raise UnitNotFoundError()

        unit.name = name

        try:
            await self.session.flush()
        except IntegrityError:
            raise UnitAlreadyExistsError()

    async def delete_unit(self, unit_id: int) -> None:
        stmt = select(Unit).where(Unit.id == unit_id)
        result = await self.session.execute(stmt)
        unit = result.scalar_one_or_none()

        if unit is None:
            raise UnitNotFoundError()

        await self.session.delete(unit)
        await self.session.flush()