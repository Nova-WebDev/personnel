from typing import Optional
from redis.asyncio import Redis

from auth.core.interfaces.refresh_token_store import IRefreshTokenStore


class RefreshTokenStore(IRefreshTokenStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 60 * 60 * 24 * 30):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(token: str) -> str:
        return f"auth:refresh:{token}"

    async def get(self, token: str) -> Optional[str]:
        return await self.redis.get(self._key(token))

    async def save(self, token: str, user_id: str) -> None:
        await self.redis.set(self._key(token), user_id, ex=self.ttl)

    async def delete(self, token: str) -> None:
        await self.redis.delete(self._key(token))