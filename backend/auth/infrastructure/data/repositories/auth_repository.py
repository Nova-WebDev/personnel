from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.interfaces.auth_repository import IAuthRepository
from auth.core.entities.auth_user_entity import AuthUserEntity
from user.infrastructure.data.models.user import UserModel


class AuthRepository(IAuthRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(user: UserModel) -> AuthUserEntity:
        permissions = [
            {"level": p.level.value, "scope": p.group_id}
            for p in user.permissions
        ]

        return AuthUserEntity(
            id=user.id,
            phone_number=user.phone,
            is_blocked=user.is_blocked,
            permissions=permissions,
        )

    async def get_by_phone(self, phone_number: str) -> AuthUserEntity | None:
        stmt = (
            select(UserModel)
            .options(joinedload(UserModel.permissions))
            .where(UserModel.phone == phone_number)
        )

        result = await self._session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        if user is None:
            return None

        return self._to_entity(user)