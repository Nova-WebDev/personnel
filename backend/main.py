from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.data.init_db import init_db
from app.redis.redis_client import redis_client
from app.utils.errors import DomainError
from app.utils.logger import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from routers.app_router import router as app_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error(str(exc), exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


app.include_router(app_router, prefix="/app", tags=["app"])