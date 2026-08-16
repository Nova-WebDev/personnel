from auth.core.interfaces.auth_store import IAuthStore
from auth.core.interfaces.refresh_token_store import IRefreshTokenStore
from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.interfaces.generat_token import IGenerator


class GenerateRefreshToken:
    def __init__(self, refresh_token_store: IRefreshTokenStore, generator: IGenerator, auth_user_store: IAuthStore):
        self.refresh_token_store = refresh_token_store
        self.auth_user_store = auth_user_store
        self.generator = generator

    async def execute(self, data: AuthSessionEntity) -> str:
        token = self.generator.generate()
        await self.refresh_token_store.save(token, data.public_id)
        await self.auth_user_store.save(data)
        return token
