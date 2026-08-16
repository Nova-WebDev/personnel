from redis.asyncio import Redis
from app.settings import settings


class RedisClient:
    def __init__(self):
        self.client = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            encoding="utf-8",
            db=0,
        )

    async def close(self):
        await self.client.close()

redis_client = RedisClient().client
