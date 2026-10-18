import secrets

from fastapi import Header

from app.settings import settings
from app.utils.errors import InvalidApiKeyError


async def verify_cron_api_key(x_api_key: str = Header(...)) -> None:
    if not secrets.compare_digest(x_api_key, settings.cron_api_key):
        raise InvalidApiKeyError()