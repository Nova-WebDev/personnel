from redis.asyncio import Redis
from app.interfaces.rate_limiter import IRateLimiter

INCREMENT_WITH_TTL = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return current
"""


class RedisIPRateLimiter(IRateLimiter):
    def __init__(self, redis: Redis, max_requests: int, window_seconds: int):
        self.redis = redis
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._increment = redis.register_script(INCREMENT_WITH_TTL)

    @staticmethod
    def _key(scope: str, identifier: str) -> str:
        return f"rate_limit:{scope}:{identifier}"

    async def is_allowed(self, key: str, scope: str) -> bool:
        current = await self._increment(keys=[self._key(scope, key)], args=[self.window_seconds])

        return current <= self.max_requests