from fastapi import Request

from app.redis.redis_client import redis_client
from app.rate_limit.redis_ip_rate_limiter import RedisIPRateLimiter
from app.utils.errors import TooManyRequestsError


def rate_limit(scope: str, max_requests: int = 30, window_seconds: int = 60):
    async def dependency(request: Request) -> None:
        redis = await redis_client.get_client()
        limiter = RedisIPRateLimiter(redis, max_requests, window_seconds)

        ip = request.headers.get("X-Real-IP") or (request.client.host if request.client else "unknown")
        allowed = await limiter.is_allowed(ip, scope)

        if not allowed:
            raise TooManyRequestsError()

    return dependency