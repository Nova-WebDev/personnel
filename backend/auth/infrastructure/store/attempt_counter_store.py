from redis.asyncio import Redis
from auth.core.interfaces.auth_attempt_counter import IAttemptCounter


class AttemptCounterStore(IAttemptCounter):
    def __init__(self, redis: Redis, ttl_seconds: int = 300):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(key: str) -> str:
        return f"auth:attempt:{key}"

    async def increment(self, key: str) -> int:
        redis_key = self._key(key)
        attempts = await self.redis.incr(redis_key)

        if attempts == 1:
            await self.redis.expire(redis_key, self.ttl)

        return attempts

    async def reset(self, key: str):
        await self.redis.delete(self._key(key))