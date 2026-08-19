import uuid

from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from personnel.core.interfaces.personnel_repository import IPersonnelRepository

from personnel.core.entities.branch_entity import BranchEntity
from personnel.core.entities.unit_entity import UnitEntity
from personnel.core.entities.branch_with_units_entity import BranchWithUnitsEntity
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition
from personnel.core.entities.personnel_order_by import PersonnelOrderBy
from personnel.core.entities.personnel_detail_entity import PersonnelDetailEntity

from personnel.core.errors.personnel_errors import (
    BranchAlreadyExistsError,
    BranchNotFoundError,
    UnitAlreadyExistsError,
    UnitNotFoundError,
    PersonnelIdAlreadyExistsError,
    PersonnelNotFoundError,
)

from personnel.infrastructure.data.models import Branch, Unit, Personnel


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

    async def get_all_branches_with_units(self) -> list[BranchWithUnitsEntity]:
        stmt = select(Branch).options(selectinload(Branch.units))
        result = await self.session.execute(stmt)
        branches = result.scalars().all()

        return [
            BranchWithUnitsEntity(
                id=branch.id,
                name=branch.name,
                units=[
                    UnitEntity(id=unit.id, name=unit.name, branch_id=unit.branch_id)
                    for unit in branch.units
                ],
            )
            for branch in branches
        ]

    async def create_personnel(
            self,
            personnel_id: str,
            first_name: str,
            last_name: str,
            branch_id: int,
            unit_id: int | None,
            photo_path: str | None,
            position: PersonnelPosition | None,
    ) -> PersonnelEntity:
        personnel = Personnel(
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            photo_path=photo_path,
            position=position,
        )
        self.session.add(personnel)

        try:
            await self.session.flush()
        except IntegrityError as e:
            error_message = str(e.orig) if e.orig else ""
            if "personnel_id" in error_message:
                raise PersonnelIdAlreadyExistsError()
            if "unit_id" in error_message:
                raise UnitNotFoundError()
            raise BranchNotFoundError()

        return PersonnelEntity(
            uuid=personnel.uuid,
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            photo_path=photo_path,
            position=position,
            is_blocked=False,
        )

    async def update_personnel(
            self,
            personnel_uuid: uuid.UUID,
            personnel_id: str,
            first_name: str,
            last_name: str,
            branch_id: int,
            unit_id: int | None,
            position: PersonnelPosition | None,
            photo_path: str | None,
    ) -> PersonnelEntity:
        stmt = select(Personnel).where(Personnel.uuid == personnel_uuid)
        result = await self.session.execute(stmt)
        personnel = result.scalar_one_or_none()

        if personnel is None:
            raise PersonnelNotFoundError()

        personnel.personnel_id = personnel_id
        personnel.first_name = first_name
        personnel.last_name = last_name
        personnel.branch_id = branch_id
        personnel.unit_id = unit_id
        personnel.position = position
        personnel.photo_path = photo_path

        try:
            await self.session.flush()
        except IntegrityError as e:
            error_message = str(e.orig) if e.orig else ""
            if "personnel_id" in error_message:
                raise PersonnelIdAlreadyExistsError()
            if "unit_id" in error_message:
                raise UnitNotFoundError()
            raise BranchNotFoundError()

        is_blocked_result: bool = personnel.is_blocked

        return PersonnelEntity(
            uuid=personnel_uuid,
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            photo_path=photo_path,
            position=position,
            is_blocked=is_blocked_result,
        )



    async def set_personnel_block_status(self, personnel_uuid: uuid.UUID, is_blocked: bool) -> None:
        stmt = select(Personnel).where(Personnel.uuid == personnel_uuid)
        result = await self.session.execute(stmt)
        personnel = result.scalar_one_or_none()

        if personnel is None:
            raise PersonnelNotFoundError()

        personnel.is_blocked = is_blocked
        await self.session.flush()

    async def count_personnel(self, search: str | None) -> int:
        stmt = select(func.count()).select_from(Personnel)

        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    Personnel.first_name.ilike(pattern),
                    Personnel.last_name.ilike(pattern),
                )
            )

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_personnel_paginated(
            self,
            offset: int,
            limit: int,
            search: str | None,
            order_by: PersonnelOrderBy,
            descending: bool,
    ) -> list[PersonnelEntity]:
        stmt = select(Personnel)

        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    Personnel.first_name.ilike(pattern),
                    Personnel.last_name.ilike(pattern),
                )
            )

        order_column = getattr(Personnel, order_by.value)
        stmt = stmt.order_by(order_column.desc() if descending else order_column.asc())
        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [
            PersonnelEntity(
                uuid=row.uuid,
                personnel_id=row.personnel_id,
                first_name=row.first_name,
                last_name=row.last_name,
                branch_id=row.branch_id,
                unit_id=row.unit_id,
                photo_path=row.photo_path,
                position=row.position,
                is_blocked=row.is_blocked,
            )
            for row in rows
        ]

    async def update_photo_path(self, personnel_uuid: uuid.UUID, photo_path: str) -> None:
        stmt = select(Personnel).where(Personnel.uuid == personnel_uuid)
        result = await self.session.execute(stmt)
        personnel = result.scalar_one_or_none()

        if personnel is None:
            raise PersonnelNotFoundError()

        personnel.photo_path = photo_path
        await self.session.flush()

    async def get_by_uuid(self, personnel_uuid: uuid.UUID) -> PersonnelEntity | None:
        stmt = select(Personnel).where(Personnel.uuid == personnel_uuid)
        result = await self.session.execute(stmt)
        personnel = result.scalar_one_or_none()

        if personnel is None:
            return None

        return PersonnelEntity(
            uuid=personnel.uuid,
            personnel_id=personnel.personnel_id,
            first_name=personnel.first_name,
            last_name=personnel.last_name,
            branch_id=personnel.branch_id,
            unit_id=personnel.unit_id,
            photo_path=personnel.photo_path,
            position=personnel.position,
            is_blocked=personnel.is_blocked,
        )

    async def get_personnel_detail(self, personnel_uuid: uuid.UUID) -> PersonnelDetailEntity | None:
        stmt = (
            select(
                Personnel,
                Branch.name.label("branch_name"),
                Unit.name.label("unit_name"),
            )
            .outerjoin(Branch, Personnel.branch_id == Branch.id)
            .outerjoin(Unit, Personnel.unit_id == Unit.id)
            .where(Personnel.uuid == personnel_uuid)
        )
        result = await self.session.execute(stmt)
        row = result.first()

        if row is None:
            return None

        personnel, branch_name, unit_name = row

        return PersonnelDetailEntity(
            uuid=personnel.uuid,
            personnel_id=personnel.personnel_id,
            first_name=personnel.first_name,
            last_name=personnel.last_name,
            photo_path=personnel.photo_path,
            position=personnel.position,
            is_blocked=personnel.is_blocked,
            branch_name=branch_name,
            unit_name=unit_name,
        )