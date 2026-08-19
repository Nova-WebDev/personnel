from fastapi import Request

from personnel.infrastructure.rate_limit.redis_ip_rate_limiter import RedisIPRateLimiter
from personnel.core.errors.personnel_errors import TooManyRequestsError
from app.redis.redis_client import redis_client


def rate_limit(scope: str, max_requests: int = 30, window_seconds: int = 60):
    async def dependency(request: Request):
        limiter = RedisIPRateLimiter(redis_client, max_requests, window_seconds)
        ip = request.headers.get("X-Real-IP") or (request.client.host if request.client else "unknown")

        allowed = await limiter.is_allowed(ip, scope)

        if not allowed:
            raise TooManyRequestsError()

    return dependency