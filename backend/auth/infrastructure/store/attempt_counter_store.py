from redis.asyncio import Redis
from auth.core.interfaces.auth_attempt_counter import IAttemptCounter


class AttemptCounterStore(IAttemptCounter):
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _key(key: str) -> str:
        return f"auth:attempt:{key}"

    async def increment(self, key: str) -> int:
        return await self.redis.incr(self._key(key))

    async def reset(self, key: str):
        await self.redis.delete(self._key(key))
