from abc import ABC, abstractmethod


class IIPRateLimiter(ABC):
    @abstractmethod
    async def is_allowed(self, ip: str, scope: str) -> bool:
        pass