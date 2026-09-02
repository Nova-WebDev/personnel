import asyncio
import json
from typing import Callable, Awaitable

from message_broker.redis_client import redis_client
from message_broker.event_entity import EventEntity
from utils.logger import logger


class RedisSubscriber:
    CHANNEL = "ws:events"

    def __init__(self, on_event: Callable[[EventEntity], Awaitable[None]]):
        self.on_event = on_event

    async def start(self) -> None:
        client = await redis_client.get_client()
        pubsub = client.pubsub()
        await pubsub.subscribe(self.CHANNEL)

        while True:
            try:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=0.5
                )

                if not message:
                    await asyncio.sleep(0.01)
                    continue

                raw = message["data"]
                data = json.loads(raw)

                event = EventEntity(**data)
                await self.on_event(event)

            except Exception as e:
                logger.error(f"[RedisSubscriber] Error: {e}", exc_info=True)
                await asyncio.sleep(1)