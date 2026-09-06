from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.interfaces.user_repository import IUserRepository
from user.infrastructure.data.models.user import UserModel
from user.infrastructure.data.models.unit import UnitModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_ids_by_branch(self, branch_id: str) -> list[str]:
        stmt = (
            select(UserModel.id)
            .join(UnitModel, UserModel.unit_id == UnitModel.id)
            .where(UnitModel.branch_id == branch_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_ids_by_unit(self, unit_id: str) -> list[str]:
        stmt = select(UserModel.id).where(UserModel.unit_id == unit_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())