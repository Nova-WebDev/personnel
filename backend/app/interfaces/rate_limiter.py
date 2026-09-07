from abc import ABC, abstractmethod


class IRateLimiter(ABC):
    @abstractmethod
    async def is_allowed(self, key: str, scope: str) -> bool:
        pass