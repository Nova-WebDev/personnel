from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth.send_code_request import SendCodeRequest
from schemas.auth.token_response import TokenResponse
from schemas.auth.verify_code_request import VerifyCodeRequest
from schemas.auth.refresh_request import RefreshRequest
from schemas.auth.logout_request import LogoutRequest

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

from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.errors.auth_errors import InvalidVerificationCodeError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-code")
async def send_code(
    payload: SendCodeRequest,
    session: AsyncSession = Depends(get_session),
):
    validate_phone_uc = get_validate_phone_uc(session)
    send_code_uc = get_send_code_phone_uc()

    user_entity = await validate_phone_uc.execute(payload.phone_number)

    session_entity = AuthSessionEntity(
        public_id=user_entity.public_id,
        phone_number=user_entity.phone_number,
        role=user_entity.role,
    )

    await send_code_uc.execute(session_entity)

    return {
        "success": True,
        "user": {
            "public_id": session_entity.public_id,
            "phone_number": session_entity.phone_number,
            "role": session_entity.role,
        }
    }


@router.post("/verify-code/", response_model=TokenResponse)
async def verify_code(payload: VerifyCodeRequest):
    verify_code_uc = get_verify_phone_verification_code_uc()
    generate_refresh_uc = get_generate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    user_identity = await verify_code_uc.execute(
        phone=payload.phone_number,
        code=payload.code,
    )

    if user_identity is None:
        raise InvalidVerificationCodeError()

    refresh_token_entity = await generate_refresh_uc.execute(user_identity)
    access_token = await generate_access_uc.execute(user_identity)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_entity,
    )


@router.post("/refresh/", response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest):
    rotate_uc = get_rotate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    token, user_identity = await rotate_uc.execute(payload.refresh_token)
    access_token = await generate_access_uc.execute(user_identity)

    return TokenResponse(
        access_token=access_token,
        refresh_token=token,
    )


@router.post("/log-out/")
async def logout(payload: LogoutRequest):
    logout_uc = get_logout_refresh_token_uc()

    await logout_uc.execute(payload.refresh_token)
    return {"detail": "Logged out"}