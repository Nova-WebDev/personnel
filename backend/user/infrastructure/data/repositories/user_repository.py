from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.interfaces.user_repository import IUserRepository
from user.infrastructure.data.models.user import UserModel
from user.infrastructure.data.models.unit import UnitModel
from user.infrastructure.data.models.branch import BranchModel
from user.core.entities.user_with_location import UserWithLocation


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

    async def get_all_with_location(self) -> list[UserWithLocation]:
        stmt = self._select_with_location()
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.all()]

    async def get_by_unit_ids_with_location(self, unit_ids: list[str]) -> list[UserWithLocation]:
        stmt = self._select_with_location().where(UserModel.unit_id.in_(unit_ids))
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.all()]

    @staticmethod
    def _select_with_location():
        return (
            select(UserModel, UnitModel.name, BranchModel.id, BranchModel.name)
            .outerjoin(UnitModel, UserModel.unit_id == UnitModel.id)
            .outerjoin(BranchModel, UnitModel.branch_id == BranchModel.id)
        )

    @staticmethod
    def _to_entity(row) -> UserWithLocation:
        user, unit_name, branch_id, branch_name = row

        return UserWithLocation(
            id=user.id,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            personnel_code=user.personnel_code,
            rfid_card_id=user.rfid_card_id,
            photo_path=user.photo_path,
            is_blocked=user.is_blocked,
            created_at=user.created_at,
            unit_id=user.unit_id,
            unit_name=unit_name,
            branch_id=branch_id,
            branch_name=branch_name,
        )