from redis.asyncio import Redis
from app.interfaces.rate_limiter import IRateLimiter


class RedisIPRateLimiter(IRateLimiter):
    def __init__(self, redis: Redis, max_requests: int, window_seconds: int):
        self.redis = redis
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    @staticmethod
    def _key(scope: str, identifier: str) -> str:
        return f"rate_limit:{scope}:{identifier}"

    async def is_allowed(self, key: str, scope: str) -> bool:
        redis_key = self._key(scope, key)
        current = await self.redis.incr(redis_key)

        if current == 1:
            await self.redis.expire(redis_key, self.window_seconds)

        return current <= self.max_requests