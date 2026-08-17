from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.interfaces.auth_repository import IAuthRepository
from auth.core.entities.auth_user_entity import AuthUserEntity
from auth.infrastructure.data.models import User


class AuthRepository(IAuthRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(user: User | None) -> AuthUserEntity | None:
        if user is None:
            return None

        return AuthUserEntity(
            phone_number=user.phone,
            public_id=str(user.public_id),
            role=user.role,
            is_blocked=user.is_blocked,
        )

    async def get_by_phone(self, phone_number: str) -> AuthUserEntity | None:
        stmt = (
            select(User)
            .where(User.phone == phone_number)
        )

        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        return self._to_entity(user)

