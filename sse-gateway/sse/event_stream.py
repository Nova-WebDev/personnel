import asyncio
import time
from typing import AsyncIterator

from settings import settings
from sse.sse_protocol import format_comment, format_event, format_retry

HEARTBEAT_COMMENT = "heartbeat"


class EventStream:
    def __init__(self, public_id: str, deadline: int):
        self.public_id = public_id
        self.deadline = deadline
        self._queue: asyncio.Queue[dict | None] = asyncio.Queue(maxsize=settings.stream_queue_size)
        self._closed = False

    def offer(self, payload: dict) -> None:
        if self._closed:
            return

        self._push(payload)

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        self._force_push(None)

    async def __aiter__(self) -> AsyncIterator[str]:
        yield format_retry(settings.client_retry_ms)

        while True:
            remaining = self.deadline - time.time()
            if remaining <= 0:
                return

            try:
                payload = await asyncio.wait_for(self._queue.get(), min(settings.heartbeat_interval, remaining))
            except TimeoutError:
                yield format_comment(HEARTBEAT_COMMENT)
                continue

            if payload is None:
                return

            yield format_event(payload["event"], payload)

    def _push(self, payload: dict) -> None:
        if self._queue.full():
            self.close()
            return

        self._queue.put_nowait(payload)

    def _force_push(self, payload: dict | None) -> None:
        if self._queue.full():
            self._queue.get_nowait()

        self._queue.put_nowait(payload)
