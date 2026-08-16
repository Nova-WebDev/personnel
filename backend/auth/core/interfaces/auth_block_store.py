from abc import ABC, abstractmethod


class IBlockStore(ABC):
    @abstractmethod
    async def block(self, public_id: str, seconds: int):
        pass

    @abstractmethod
    async def is_blocked(self, public_id: str) -> bool:
        pass
