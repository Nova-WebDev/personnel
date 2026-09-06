from sqlalchemy.ext.asyncio import AsyncSession

from user.core.interfaces.branch_repository import IBranchRepository
from user.core.entities.branch import Branch
from user.infrastructure.data.models.branch import BranchModel
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