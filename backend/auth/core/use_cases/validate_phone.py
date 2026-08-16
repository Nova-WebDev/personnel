from auth.core.entities.auth_user_entity import AuthUserEntity
from auth.core.interfaces.auth_repository import IAuthRepository
from auth.core.errors.auth_errors import (
    InvalidPhoneFormatError,
    UserNotFoundError,
    UserBlockedError,
)

class ValidatePhone:
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    async def execute(self, phone_number: str) -> AuthUserEntity:
        if len(phone_number) != 11 or not phone_number.isdigit():
            raise InvalidPhoneFormatError()

        user = await self.auth_repository.get_by_phone(phone_number)

        if user is None:
            raise UserNotFoundError()

        if user.is_blocked:
            raise UserBlockedError()

        return user