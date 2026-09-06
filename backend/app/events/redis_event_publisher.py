import json

from app.redis.redis_client import RedisClient
from app.interfaces.event_publisher import IEventPublisher

CHANNEL = "ws:events"


class RedisEventPublisher(IEventPublisher):
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def publish(
        self,
        event: str,
        scope: str,
        data: dict,
        meta: dict | None = None,
        targets: list[str] | None = None,
    ) -> None:
        payload = {
            "targets": targets or ["*"],
            "event": event,
            "scope": scope,
            "meta": meta or {},
            "data": data,
        }

        await self.redis_client.publish(CHANNEL, json.dumps(payload))