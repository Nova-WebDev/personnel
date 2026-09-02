from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/time")
async def server_time():
    return {"server_time": datetime.now(timezone.utc).isoformat()}