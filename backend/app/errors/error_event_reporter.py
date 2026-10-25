import asyncio
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone

from app.interfaces.event_publisher import IEventPublisher
from app.utils.logger import logger

QUEUE_SIZE = 100
STEP_TIMEOUT_SECONDS = 3
THROTTLE_SECONDS = 60
ADMIN_CACHE_SECONDS = 300
THROTTLE_MAX_KEYS = 500
MESSAGE_MAX_LENGTH = 300


class ErrorEventReporter:
    def __init__(
        self,
        event_publisher: IEventPublisher,
        admin_ids_provider: Callable[[], Awaitable[list[str]]],
    ):
        self._event_publisher = event_publisher
        self._admin_ids_provider = admin_ids_provider
        self._queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=QUEUE_SIZE)
        self._worker: asyncio.Task | None = None
        self._last_sent: dict[str, float] = {}
        self._admin_ids: list[str] = []
        self._admin_ids_loaded_at = 0.0

    def start(self) -> None:
        self._worker = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._worker is None:
            return
        self._worker.cancel()
        try:
            await self._worker
        except asyncio.CancelledError:
            pass

    def report(self, method: str, path: str, exc: Exception) -> None:
        item = {
            "method": method,
            "path": path,
            "error_type": type(exc).__name__,
            "message": str(exc)[:MESSAGE_MAX_LENGTH],
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            self._queue.put_nowait(item)
        except asyncio.QueueFull:
            pass

    async def _run(self) -> None:
        while True:
            item = await self._queue.get()
            try:
                await asyncio.wait_for(self._handle(item), timeout=STEP_TIMEOUT_SECONDS * 2)
            except Exception as error:
                logger.error(f"[ErrorEventReporter] Failed to report error event: {error}")

    async def _handle(self, item: dict) -> None:
        if not self._allow(item):
            return

        admin_ids = await self._get_admin_ids()
        if not admin_ids:
            return

        await asyncio.wait_for(
            self._event_publisher.publish(
                event="system.error",
                scope="system",
                data=item,
                targets=admin_ids,
            ),
            timeout=STEP_TIMEOUT_SECONDS,
        )

    def _allow(self, item: dict) -> bool:
        key = f"{item['method']}:{item['path']}:{item['error_type']}"
        now = time.monotonic()

        last = self._last_sent.get(key)
        if last is not None and now - last < THROTTLE_SECONDS:
            return False

        if len(self._last_sent) >= THROTTLE_MAX_KEYS:
            self._last_sent = {
                k: v for k, v in self._last_sent.items() if now - v < THROTTLE_SECONDS
            }

        self._last_sent[key] = now
        return True

    async def _get_admin_ids(self) -> list[str]:
        now = time.monotonic()
        if self._admin_ids and now - self._admin_ids_loaded_at < ADMIN_CACHE_SECONDS:
            return self._admin_ids

        try:
            self._admin_ids = await asyncio.wait_for(
                self._admin_ids_provider(), timeout=STEP_TIMEOUT_SECONDS
            )
            self._admin_ids_loaded_at = now
        except Exception as error:
            logger.error(f"[ErrorEventReporter] Failed to load admin ids: {error}")

        return self._admin_ids