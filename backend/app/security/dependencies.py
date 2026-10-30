from dataclasses import dataclass

from fastapi import Cookie, HTTPException

from .token_validator import TokenValidationError, TokenValidator

_validator = TokenValidator()


@dataclass(frozen=True)
class CurrentUser:
    id: str
    phone_number: str
    permissions: list[dict]


async def get_current_user(access_token: str = Cookie(None)) -> CurrentUser:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = _validator.validate(access_token)
    except TokenValidationError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return CurrentUser(
        id=payload["id"],
        phone_number=payload["phone_number"],
        permissions=payload["permissions"],
    )