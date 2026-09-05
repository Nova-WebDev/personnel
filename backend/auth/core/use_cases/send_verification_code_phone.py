from auth.core.errors.auth_errors import PhoneTemporarilyBlockedError
from auth.core.interfaces.code_generator import ICodeGenerator
from auth.core.interfaces.sms_sender import ISmsSender
from auth.core.interfaces.auth_block_store import IBlockStore
from auth.core.interfaces.auth_code_store import ICodeStore
from auth.core.entities.auth_session_entity import AuthSessionEntity

SHORT_BLOCK_SECONDS = 10
SEND_SUCCESS_BLOCK_SECONDS = 60


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

        if not await self.block_store.try_block(phone, SHORT_BLOCK_SECONDS):
            raise PhoneTemporarilyBlockedError()

        code = await self.code_generator.generate()

        await self.code_store.save(
            phone,
            {
                "code": code,
                "user": {
                    "id": user.id,
                    "phone_number": phone,
                    "permissions": user.permissions,
                },
            }
        )

        await self.sms_sender.send(phone, code)

        await self.block_store.force_block(phone, SEND_SUCCESS_BLOCK_SECONDS)

        return {
            "phone_number": phone,
            "sent": True
        }