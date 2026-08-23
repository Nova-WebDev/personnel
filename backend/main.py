from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.data.init_db import init_db
from app.redis.redis_client import redis_client
from app.utils.logger import logger

from auth.core.errors.auth_errors import DomainError

from routers.health import router as health_router
from routers.auth import router as auth_router
from routers.personnel import router as personnel_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    if exc.status_code != 200:
        logger.error(str(exc), exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(personnel_router)