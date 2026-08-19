import uuid
from abc import ABC, abstractmethod


class IQRRateLimiter(ABC):
    @abstractmethod
    async def is_allowed(self, personnel_uuid: uuid.UUID) -> bool:
        pass