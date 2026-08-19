from redis.asyncio import Redis

from personnel.core.interfaces.ip_rate_limiter import IIPRateLimiter


class RedisIPRateLimiter(IIPRateLimiter):
    def __init__(self, redis_client: Redis, max_requests: int = 30, window_seconds: int = 60):
        self.redis_client = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, ip: str, scope: str) -> bool:
        key = f"ratelimit:{scope}:{ip}"
        count = await self.redis_client.incr(key)

        if count == 1:
            await self.redis_client.expire(key, self.window_seconds)

        return count <= self.max_requests