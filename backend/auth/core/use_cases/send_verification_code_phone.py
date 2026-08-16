from app.utils.logger import logger
from auth.core.errors.auth_errors import PhoneTemporarilyBlockedError
from auth.core.interfaces.code_generator import ICodeGenerator
from auth.core.interfaces.sms_sender import ISmsSender
from auth.core.interfaces.auth_block_store import IBlockStore
from auth.core.interfaces.auth_code_store import ICodeStore
from auth.core.entities.auth_session_entity import AuthSessionEntity


class SendVerificationCodePhone:
    def __init__(
        self,
        block_store: IBlockStore,
        code_generator: ICodeGenerator,
        code_store: ICodeStore,
        sms_sender: ISmsSender
    ):
        self.block_store = block_store
        self.code_generator = code_generator
        self.code_store = code_store
        self.sms_sender = sms_sender

    async def execute(self, user: AuthSessionEntity):
        phone = user.phone_number

        if await self.block_store.is_blocked(phone):
            raise PhoneTemporarilyBlockedError()

        code = await self.code_generator.generate()

        await self.code_store.save(
            phone,
            {
                "code": code,
                "user": {
                    "public_id": user.public_id,
                    "role": user.role,
                    "phone_number": phone,
                },
            }
        )

        await self.block_store.block(phone, 60)

        await self.sms_sender.send(phone, code)


        logger.error(code)
        return {
            "phone_number": phone,
            "sent": True
        }