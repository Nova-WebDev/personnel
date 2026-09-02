import asyncio
import redis.asyncio as redis
from settings import settings
from utils.logger import logger


class RedisClient:
    def __init__(self) -> None:
        self._url = settings.redis_url
        self._client: redis.Redis | None = None

    async def get_client(self) -> redis.Redis:
        if self._client is not None:
            return self._client

        backoff = 1
        max_backoff = 30

        while True:
            try:
                client = redis.from_url(
                    self._url,
                    decode_responses=True,
                )
                await client.ping()
                self._client = client
                return client

            except Exception as e:
                logger.error(f"[Redis] Connection failed: {e}. Retrying in {backoff}s...")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)

    async def publish(self, channel: str, message: str):
        client = await self.get_client()
        await client.publish(channel, message)


redis_client = RedisClient()