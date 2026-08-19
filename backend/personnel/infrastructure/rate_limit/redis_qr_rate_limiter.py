import uuid

from redis.asyncio import Redis

from personnel.core.interfaces.qr_rate_limiter import IQRRateLimiter


class RedisQRRateLimiter(IQRRateLimiter):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def is_allowed(self, personnel_uuid: uuid.UUID) -> bool:
        key = f"qr:cooldown:{personnel_uuid}"
        was_set = await self.redis_client.set(key, "1", nx=True, ex=30)
        return bool(was_set)