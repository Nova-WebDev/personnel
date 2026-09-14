from redis.asyncio import Redis
from meals.core.interfaces.cache_store import ICacheStore


class RedisCacheStore(ICacheStore):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def set(self, key: str, value: str) -> None:
        await self.redis.set(key, value)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)