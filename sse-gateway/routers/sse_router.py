from typing import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from auth.dependencies import get_token_payload
from auth.token_payload import TokenPayload
from sse.connection_store import connection_store
from sse.event_stream import EventStream

router = APIRouter()

STREAM_HEADERS = {
    "Cache-Control": "no-cache, no-store, no-transform",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


@router.get("/events")
async def stream_events(payload: TokenPayload = Depends(get_token_payload)) -> StreamingResponse:
    stream = EventStream(payload.public_id, payload.exp)
    connection_store.add(stream)

    return StreamingResponse(
        _drain(stream),
        media_type="text/event-stream",
        headers=STREAM_HEADERS,
    )


async def _drain(stream: EventStream) -> AsyncIterator[str]:
    try:
        async for chunk in stream:
            yield chunk
    finally:
        connection_store.remove(stream)
