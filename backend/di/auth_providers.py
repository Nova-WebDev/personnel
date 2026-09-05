from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client

from auth.core.use_cases.validate_phone import ValidatePhone
from auth.core.use_cases.send_verification_code_phone import SendVerificationCodePhone
from auth.core.use_cases.verify_phone_verification_code import VerifyPhoneVerificationCode
from auth.core.use_cases.generate_refresh_token import GenerateRefreshToken
from auth.core.use_cases.generate_access_token import GenerateAccessToken
from auth.core.use_cases.rotate_refresh_token import RotateRefreshToken
from auth.core.use_cases.logout_refresh_token import LogoutRefreshToken

from auth.infrastructure.data.repositories.auth_repository import AuthRepository

from auth.infrastructure.store.code_store import CodeStore
from auth.infrastructure.store.block_store import BlockStore
from auth.infrastructure.store.attempt_counter_store import AttemptCounterStore
from auth.infrastructure.store.refresh_token_store import RefreshTokenStore
from auth.infrastructure.store.auth_store import AuthStore

from auth.infrastructure.signing.token_header_generator import TokenHeaderGenerator
from auth.infrastructure.signing.token_payload_generator import TokenPayloadGenerator
from auth.infrastructure.signing.token_signer import TokenSigner

from auth.infrastructure.sms.kavenegar_sms_sender import KavenegarSmsSender

from auth.utility.code_generator import CodeGenerator
from auth.utility.secure_token_generator import SecureTokenGenerator


def get_validate_phone_uc(session: AsyncSession) -> ValidatePhone:
    return ValidatePhone(
        auth_repository=AuthRepository(session)
    )


async def get_send_code_phone_uc() -> SendVerificationCodePhone:
    redis = await redis_client.get_client()
    return SendVerificationCodePhone(
        block_store=BlockStore(redis),
        code_generator=CodeGenerator(),
        code_store=CodeStore(redis),
        sms_sender=KavenegarSmsSender(),
    )


async def get_verify_phone_verification_code_uc() -> VerifyPhoneVerificationCode:
    redis = await redis_client.get_client()
    return VerifyPhoneVerificationCode(
        code_store=CodeStore(redis),
        block_store=BlockStore(redis),
        attempt_counter=AttemptCounterStore(redis),
    )


async def get_generate_refresh_token_uc() -> GenerateRefreshToken:
    redis = await redis_client.get_client()
    return GenerateRefreshToken(
        refresh_token_store=RefreshTokenStore(redis),
        auth_user_store=AuthStore(redis),
        generator=SecureTokenGenerator(),
    )


def get_generate_access_token_uc() -> GenerateAccessToken:
    return GenerateAccessToken(
        header_generator=TokenHeaderGenerator(),
        payload_generator=TokenPayloadGenerator(),
        signer=TokenSigner(),
    )


async def get_rotate_refresh_token_uc() -> RotateRefreshToken:
    redis = await redis_client.get_client()
    return RotateRefreshToken(
        refresh_token_store=RefreshTokenStore(redis),
        auth_user_store=AuthStore(redis),
        generator=SecureTokenGenerator(),
    )


async def get_logout_refresh_token_uc() -> LogoutRefreshToken:
    redis = await redis_client.get_client()
    return LogoutRefreshToken(
        store=RefreshTokenStore(redis)
    )