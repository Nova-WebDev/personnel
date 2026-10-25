from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.data.init_db import init_db
from app.redis.redis_client import redis_client
from app.utils.errors import DomainError
from app.utils.logger import logger
from di.error_reporting_providers import error_event_reporter

from routers.app_router import router as app_router
from routers.auth import router as auth_router
from routers.meals_router import router as meals_router
from routers.user_router import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    error_event_reporter.start()
    yield
    await error_event_reporter.stop()
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error(str(exc), exc_info=True)
        error_event_reporter.report(request.method, request.url.path, exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(str(exc), exc_info=True)
    error_event_reporter.report(request.method, request.url.path, exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(app_router, prefix="/app", tags=["app"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(meals_router, prefix="/meals", tags=["meals"])