import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from message_broker.redis_client import redis_client
from message_broker.redis_subscriber import RedisSubscriber
from routers.health_router import router as health_router
from routers.sse_router import router as sse_router
from sse.connection_store import connection_store
from sse.event_dispatcher import event_dispatcher


@asynccontextmanager
async def lifespan(_app: FastAPI):
    subscriber_task = asyncio.create_task(
        RedisSubscriber(on_event=event_dispatcher.dispatch).run()
    )

    yield

    subscriber_task.cancel()

    try:
        await subscriber_task
    except asyncio.CancelledError:
        pass

    connection_store.close_all()
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(sse_router)
app.include_router(health_router)
