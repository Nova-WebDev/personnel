import re

from auth.core.entities.auth_session_entity import AuthSessionEntity
from auth.core.interfaces.auth_repository import IAuthRepository
from auth.core.errors.auth_errors import (
    InvalidPhoneFormatError,
    UserNotFoundError,
    UserBlockedError,
)

PHONE_PATTERN = re.compile(r"^09\d{9}$")


class ValidatePhone:
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    async def execute(self, phone_number: str) -> AuthSessionEntity:
        if not PHONE_PATTERN.match(phone_number):
            raise InvalidPhoneFormatError()

        user = await self.auth_repository.get_by_phone(phone_number)

        if user is None:
            raise UserNotFoundError()

        if user.is_blocked:
            raise UserBlockedError()

        return AuthSessionEntity(
            id=user.id,
            phone_number=user.phone_number,
            is_blocked=user.is_blocked,
            permissions=user.permissions,
        )