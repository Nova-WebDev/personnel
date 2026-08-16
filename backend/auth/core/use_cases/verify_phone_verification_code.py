from typing import Optional

from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.interfaces.auth_block_store import IBlockStore
from auth.core.interfaces.auth_code_store import ICodeStore
from auth.core.interfaces.auth_attempt_counter import IAttemptCounter
from auth.core.errors.auth_errors import (
    InvalidVerificationCodeError,
)


class VerifyPhoneVerificationCode:
    def __init__(
        self,
        code_store: ICodeStore,
        block_store: IBlockStore,
        attempt_counter: IAttemptCounter,
        max_attempts: int = 5,
    ):
        self.code_store = code_store
        self.block_store = block_store
        self.attempt_counter = attempt_counter
        self.max_attempts = max_attempts

    async def execute(self, phone: str, code: str) -> Optional[AuthSessionEntity]:


        session = await self.code_store.get(phone)

        if session is None:
            attempts = await self.attempt_counter.increment(phone)

            if attempts >= self.max_attempts:
                await self.block_store.block(phone, 300)
                await self.code_store.delete(phone)

            raise InvalidVerificationCodeError()

        stored_code = session.get("code")

        if stored_code != code:
            attempts = await self.attempt_counter.increment(phone)

            if attempts >= self.max_attempts:
                await self.block_store.block(phone, 300)
                await self.code_store.delete(phone)

            raise InvalidVerificationCodeError()

        await self.code_store.delete(phone)
        await self.attempt_counter.reset(phone)

        return AuthSessionEntity(
            public_id=session["user"]["public_id"],
            phone_number=phone,
            role=session["user"]["role"],
        )