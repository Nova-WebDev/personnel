import asyncio
import redis.asyncio as redis
from settings import settings
from utils.logger import logger

INITIAL_BACKOFF = 1
MAX_BACKOFF = 30


class RedisClient:
    def __init__(self) -> None:
        self._url = settings.redis_url
        self._client: redis.Redis | None = None

    async def get_client(self) -> redis.Redis:
        if self._client is not None:
            return self._client

        backoff = INITIAL_BACKOFF

        while True:
            try:
                client = redis.from_url(
                    self._url,
                    decode_responses=True,
                    health_check_interval=30,
                )
                await client.ping()
                self._client = client
                return client

            except Exception as e:
                logger.error(f"[Redis] Connection failed: {e}. Retrying in {backoff}s...")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, MAX_BACKOFF)

    async def aclose(self) -> None:
        if self._client is None:
            return

        client, self._client = self._client, None
        await client.aclose()


redis_client = RedisClient()
