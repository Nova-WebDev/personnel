from fastapi import Header

from app.settings import settings
from app.utils.errors import InvalidApiKeyError


async def verify_personnel_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.personnel_api_key:
        raise InvalidApiKeyError()