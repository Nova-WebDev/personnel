from auth.core.interfaces.refresh_token_store import IRefreshTokenStore
from auth.core.interfaces.auth_store import IAuthStore
from auth.core.interfaces.generat_token import IGenerator
from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.errors.auth_errors import InvalidRefreshToken


class RotateRefreshToken:
    def __init__(
        self,
        refresh_token_store: IRefreshTokenStore,
        auth_user_store: IAuthStore,
        generator: IGenerator,
    ):
        self.refresh_token_store = refresh_token_store
        self.auth_user_store = auth_user_store
        self.generator = generator

    async def execute(self, old_refresh_token: str) -> tuple[str, AuthSessionEntity]:
        public_id = await self.refresh_token_store.get(old_refresh_token)
        if public_id is None:
            raise InvalidRefreshToken()

        session: AuthSessionEntity | None = await self.auth_user_store.get(public_id)
        if session is None:
            await self.refresh_token_store.delete(old_refresh_token)
            raise InvalidRefreshToken()

        new_refresh_token = self.generator.generate()
        await self.refresh_token_store.save(new_refresh_token, public_id)
        await self.refresh_token_store.delete(old_refresh_token)

        return new_refresh_token, session
