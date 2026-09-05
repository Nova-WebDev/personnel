from abc import ABC, abstractmethod
from typing import Optional
from auth.core.entities.auth_session_entity import AuthSessionEntity


class IAuthStore(ABC):
    @abstractmethod
    async def get(self, user_id: str) -> Optional[AuthSessionEntity]:
        pass

    @abstractmethod
    async def save(self, data: AuthSessionEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def update_permissions(self, user_id: str, permissions: list[dict]) -> None:
        pass