import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from websocket.websocket_handler import router as ws_router
from routers.health_router import router as health_router
from websocket.event_dispatcher import event_dispatcher
from websocket.ping_loop import ping_loop
from message_broker.redis_subscriber import RedisSubscriber


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ping_task = asyncio.create_task(ping_loop.run())
    subscriber_task = asyncio.create_task(
        RedisSubscriber(on_event=event_dispatcher.dispatch).start()
    )

    yield

    ping_task.cancel()
    subscriber_task.cancel()

    try:
        await ping_task
    except asyncio.CancelledError:
        pass

    try:
        await subscriber_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(ws_router)
app.include_router(health_router)