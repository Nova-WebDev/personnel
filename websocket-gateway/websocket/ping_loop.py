import asyncio
import time

from websocket.connection_store import connection_store
from utils.logger import logger

PING_INTERVAL = 30
PING_TIMEOUT = 45


class PingLoop:
    def __init__(self, interval: int = PING_INTERVAL, timeout: int = PING_TIMEOUT):
        self.interval = interval
        self.timeout = timeout

    async def run(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self._check_all_connections()

    async def _check_all_connections(self) -> None:
        now = time.time()

        for public_id, ws, last_pong in connection_store.all_connections():
            if last_pong and now - last_pong > self.timeout:
                await self._disconnect(public_id, ws)
                continue

            await self._send_ping(public_id, ws)

    @staticmethod
    async def _send_ping(public_id: str, ws) -> None:
        try:
            await ws.send_text("ping")
        except Exception as e:
            logger.error(f"[PingLoop] Failed to send ping to {public_id}: {e}")
            await connection_store.remove(public_id, ws)

    @staticmethod
    async def _disconnect(public_id: str, ws) -> None:
        await connection_store.remove(public_id, ws)
        try:
            await ws.close(code=4408)
        except Exception as e:
            logger.debug(f"[PingLoop] Close failed for {public_id}, likely already disconnected: {e}")


ping_loop = PingLoop()