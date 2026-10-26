from fastapi import Cookie, HTTPException

from auth.jwt_decoder import JWTDecodeError, JWTDecoder
from auth.token_payload import TokenPayload

_decoder = JWTDecoder()


async def get_token_payload(access_token: str = Cookie(None)) -> TokenPayload:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        return _decoder.decode(access_token)
    except JWTDecodeError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
