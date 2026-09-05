from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth.send_code_request import SendCodeRequest
from schemas.auth.verify_code_request import VerifyCodeRequest
from schemas.auth.refresh_request import RefreshRequest
from schemas.auth.logout_request import LogoutRequest
from schemas.auth.token_response import TokenResponse

from di.auth_providers import (
    get_validate_phone_uc,
    get_send_code_phone_uc,
    get_verify_phone_verification_code_uc,
    get_generate_refresh_token_uc,
    get_generate_access_token_uc,
    get_rotate_refresh_token_uc,
    get_logout_refresh_token_uc,
)
from app.data.db import get_session

ACCESS_TOKEN_MAX_AGE = 15 * 60

router = APIRouter()

def _set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )


@router.post("/send-code")
async def send_code(
    payload: SendCodeRequest,
    session: AsyncSession = Depends(get_session),
):
    validate_phone_uc = get_validate_phone_uc(session)
    send_code_uc = await get_send_code_phone_uc()

    session_entity = await validate_phone_uc.execute(payload.phone_number)
    await send_code_uc.execute(session_entity)

    return {"success": True, "phone_number": session_entity.phone_number}


@router.post("/verify-code", response_model=TokenResponse)
async def verify_code(
    payload: VerifyCodeRequest,
    response: Response,
):
    verify_code_uc = await get_verify_phone_verification_code_uc()
    generate_refresh_uc = await get_generate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    session_entity = await verify_code_uc.execute(
        phone=payload.phone_number,
        code=payload.code,
    )

    refresh_token_value = await generate_refresh_uc.execute(session_entity)
    access_result = await generate_access_uc.execute(session_entity)

    _set_access_cookie(response, access_result.token)

    return TokenResponse(
        refresh_token=refresh_token_value,
        access_token_expires_at=access_result.expires_at,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: RefreshRequest,
    response: Response,
):
    rotate_uc = await get_rotate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    new_refresh_token, session_entity = await rotate_uc.execute(payload.refresh_token)
    access_result = await generate_access_uc.execute(session_entity)

    _set_access_cookie(response, access_result.token)

    return TokenResponse(
        refresh_token=new_refresh_token,
        access_token_expires_at=access_result.expires_at,
    )


@router.post("/log-out")
async def logout(
    payload: LogoutRequest,
    response: Response,
):
    logout_uc = await get_logout_refresh_token_uc()
    await logout_uc.execute(payload.refresh_token)
    response.delete_cookie("access_token", path="/")
    return {"detail": "Logged out"}