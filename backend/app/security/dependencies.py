from fastapi import Cookie, HTTPException

from app.security.token_validator import token_validator, TokenValidationError


async def get_current_user(access_token: str = Cookie(None)) -> dict:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = token_validator.validate(access_token)
    except TokenValidationError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload