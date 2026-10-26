from fastapi import APIRouter

from sse.connection_store import connection_store

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok", "connections": connection_store.total()}
