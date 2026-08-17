from redis.asyncio import Redis

from app.settings import settings


redis_client: Redis = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    encoding="utf-8",
    db=0,
)