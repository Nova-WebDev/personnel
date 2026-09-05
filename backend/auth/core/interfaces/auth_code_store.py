from abc import ABC, abstractmethod
from typing import Optional


class ICodeStore(ABC):
    @abstractmethod
    async def get(self, phone_number: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def save(self, phone_number: str, data: dict):
        pass

    @abstractmethod
    async def delete(self, phone_number: str):
        pass
