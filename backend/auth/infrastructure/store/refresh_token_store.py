from typing import Optional
from redis.asyncio import Redis

from app.utils.logger import logger
from auth.core.interfaces.refresh_token_store import IRefreshTokenStore


class RefreshTokenStore(IRefreshTokenStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 60 * 60 * 24 * 30):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(token: str) -> str:
        return f"auth:refresh:{token}"

    async def get(self, token: str) -> Optional[str]:
        key = self._key(token)

        try:
            public_id = await self.redis.get(key)
            return public_id

        except Exception as e:
            logger.error(f"RefreshTokenStore.get failed: {e}")
            return None

    async def save(self, token: str, public_id: str) -> None:
        key = self._key(token)

        try:
            await self.redis.set(key, public_id, ex=self.ttl)

        except Exception as e:
            logger.error(f"RefreshTokenStore.save failed: {e}")
            return None

    async def delete(self, token: str) -> None:
        key = self._key(token)

        try:
            await self.redis.delete(key)

        except Exception as e:
            logger.error(f"RefreshTokenStore.delete failed: {e}")
            return None