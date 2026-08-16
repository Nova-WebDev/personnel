from abc import ABC, abstractmethod
from typing import Optional
from auth.core.entities.auth_session_entity import AuthSessionEntity


class IAuthStore(ABC):
    @abstractmethod
    async def get(self, public_id: str) -> Optional[AuthSessionEntity]:
        pass

    @abstractmethod
    async def save(self, data: AuthSessionEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, public_id: str) -> None:
        pass

    @abstractmethod
    async def change_role(self, public_id: str, role: int) -> None:
        pass