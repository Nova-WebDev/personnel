from redis.asyncio import Redis
from meals.core.interfaces.meal_cache import IMealCache

CACHE_KEY = "meals"


class RedisMealCache(IMealCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set(self, meal_id: str, data: str) -> None:
        await self.redis.hset(CACHE_KEY, meal_id, data)

    async def get(self, meal_id: str) -> str | None:
        return await self.redis.hget(CACHE_KEY, meal_id)

    async def get_all(self) -> dict[str, str]:
        return await self.redis.hgetall(CACHE_KEY)

    async def delete(self, meal_id: str) -> None:
        await self.redis.hdel(CACHE_KEY, meal_id)

    async def clear(self) -> None:
        await self.redis.delete(CACHE_KEY)