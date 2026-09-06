from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from user.core.interfaces.branch_repository import IBranchRepository
from user.core.entities.branch import Branch
from user.core.entities.unit import Unit
from user.core.entities.branch_with_units import BranchWithUnits
from user.infrastructure.data.models.branch import BranchModel
from user.infrastructure.data.models.unit import UnitModel
from user.core.errors.user_errors import BranchNotFoundError


class BranchRepository(IBranchRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, name: str) -> Branch:
        model = BranchModel(name=name)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)

        return Branch(id=model.id, name=model.name)

    async def update(self, branch_id: str, name: str) -> Branch:
        model = await self._session.get(BranchModel, branch_id)

        if model is None:
            raise BranchNotFoundError()

        model.name = name
        await self._session.flush()
        await self._session.refresh(model)

        return Branch(id=model.id, name=model.name)

    async def delete(self, branch_id: str) -> None:
        model = await self._session.get(BranchModel, branch_id)

        if model is None:
            raise BranchNotFoundError()

        await self._session.delete(model)
        await self._session.flush()

    async def get_all_with_units(self) -> list[BranchWithUnits]:
        stmt = select(BranchModel).options(joinedload(BranchModel.units))
        result = await self._session.execute(stmt)
        branches = result.unique().scalars().all()

        return [self._to_branch_with_units(b) for b in branches]

    async def get_by_unit_ids_with_units(self, unit_ids: list[str]) -> list[BranchWithUnits]:
        stmt = (
            select(BranchModel)
            .join(UnitModel, UnitModel.branch_id == BranchModel.id)
            .where(UnitModel.id.in_(unit_ids))
            .options(joinedload(BranchModel.units.and_(UnitModel.id.in_(unit_ids))))
        )
        result = await self._session.execute(stmt)
        branches = result.unique().scalars().all()

        return [self._to_branch_with_units(b) for b in branches]

    @staticmethod
    def _to_branch_with_units(model: BranchModel) -> BranchWithUnits:
        return BranchWithUnits(
            branch_id=model.id,
            branch_name=model.name,
            units=[Unit(id=u.id, name=u.name, branch_id=u.branch_id) for u in model.units],
        )