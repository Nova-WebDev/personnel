from abc import ABC, abstractmethod


class IQRCodeGenerator(ABC):
    @abstractmethod
    async def generate(self, data: str) -> bytes:
        pass