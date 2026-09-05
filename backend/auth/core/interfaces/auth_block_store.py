from abc import ABC, abstractmethod


class IBlockStore(ABC):
    @abstractmethod
    async def try_block(self, phone_number: str, seconds: int) -> bool:
        pass

    @abstractmethod
    async def force_block(self, phone_number: str, seconds: int) -> None:
        pass