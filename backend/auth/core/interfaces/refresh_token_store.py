from abc import ABC, abstractmethod
from typing import Optional


class IRefreshTokenStore(ABC):
    @abstractmethod
    async def get(self, token: str) -> Optional[str]:
        pass

    @abstractmethod
    async def save(self, token: str, public_id: str) -> None:
        pass

    @abstractmethod
    async def delete(self, token: str) -> None:
        pass