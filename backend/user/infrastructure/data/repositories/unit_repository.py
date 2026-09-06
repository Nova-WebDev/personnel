from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from user.core.interfaces.unit_repository import IUnitRepository
from user.core.entities.unit import Unit
from user.infrastructure.data.models.unit import UnitModel
from user.core.errors.user_errors import BranchNotFoundError, UnitNameConflictError, UnitNotFoundError


class UnitRepository(IUnitRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, name: str, branch_id: str) -> Unit:
        model = UnitModel(name=name, branch_id=branch_id)
        self._session.add(model)

        try:
            await self._session.flush()
        except IntegrityError as e:
            if "uq_unit_name_branch" in str(e.orig):
                raise UnitNameConflictError()
            raise BranchNotFoundError()

        await self._session.refresh(model)

        return Unit(id=model.id, name=model.name, branch_id=model.branch_id)

    async def update(self, unit_id: str, name: str) -> Unit:
        model = await self._session.get(UnitModel, unit_id)

        if model is None:
            raise UnitNotFoundError()

        model.name = name

        try:
            await self._session.flush()
        except IntegrityError as e:
            if "uq_unit_name_branch" in str(e.orig):
                raise UnitNameConflictError()
            raise

        await self._session.refresh(model)

        return Unit(id=model.id, name=model.name, branch_id=model.branch_id)

    async def delete(self, unit_id: str) -> None:
        model = await self._session.get(UnitModel, unit_id)

        if model is None:
            raise UnitNotFoundError()

        await self._session.delete(model)
        await self._session.flush()