from abc import ABC, abstractmethod


class IImageFormatValidator(ABC):
    @abstractmethod
    async def validate(self, file_bytes: bytes) -> None:
        pass