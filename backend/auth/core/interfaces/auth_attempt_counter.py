from abc import ABC, abstractmethod


class IAttemptCounter(ABC):
    @abstractmethod
    async def increment(self, key: str) -> int:
        pass

    @abstractmethod
    async def reset(self, key: str):
        pass
