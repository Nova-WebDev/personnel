import asyncio
from typing import Callable

from pydantic import ValidationError

from message_broker.event_entity import EventEntity
from message_broker.redis_client import redis_client
from settings import settings
from utils.logger import logger

RESUBSCRIBE_DELAY = 1


class RedisSubscriber:
    def __init__(self, on_event: Callable[[EventEntity], None]):
        self.on_event = on_event
        self.channel = settings.event_channel

    async def run(self) -> None:
        while True:
            try:
                await self._consume()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"[RedisSubscriber] Subscription lost: {e}", exc_info=True)
                await redis_client.aclose()
                await asyncio.sleep(RESUBSCRIBE_DELAY)

    async def _consume(self) -> None:
        client = await redis_client.get_client()

        async with client.pubsub() as pubsub:
            await pubsub.subscribe(self.channel)

            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                self._handle(message["data"])

    def _handle(self, raw: str) -> None:
        try:
            event = EventEntity.model_validate_json(raw)
        except ValidationError as e:
            logger.error(f"[RedisSubscriber] Discarded malformed event: {e}")
            return

        try:
            self.on_event(event)
        except Exception as e:
            logger.error(f"[RedisSubscriber] Dispatch failed for '{event.event}': {e}", exc_info=True)
