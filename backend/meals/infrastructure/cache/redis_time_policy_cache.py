from redis.asyncio import Redis
from meals.core.interfaces.time_policy_cache import ITimePolicyCache

CACHE_KEY = "meal_plan_time_policies"


class RedisTimePolicyCache(ITimePolicyCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_all(self) -> str | None:
        return await self.redis.get(CACHE_KEY)

    async def set_all(self, data: str) -> None:
        await self.redis.set(CACHE_KEY, data)

    async def clear(self) -> None:
        await self.redis.delete(CACHE_KEY)