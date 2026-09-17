from abc import ABC, abstractmethod


class ITimePolicyCache(ABC):
    @abstractmethod
    async def get_all(self) -> str | None:
        pass

    @abstractmethod
    async def set_all(self, data: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass