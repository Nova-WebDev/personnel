from abc import ABC, abstractmethod
from typing import Optional
from auth.core.entities.auth_user_entity import AuthUserEntity


class IAuthRepository(ABC):
    @abstractmethod
    async def get_by_phone(self, phone_number: str) -> Optional[AuthUserEntity]:
        pass
