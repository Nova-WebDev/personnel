from abc import ABC, abstractmethod


class IImageProcessor(ABC):
    @abstractmethod
    async def process(
        self,
        file_id: str,
        file_bytes: bytes,
        resize_to: tuple[int, int] | None = None,
        force_png: bool = True,
    ) -> None:
        pass

    @abstractmethod
    async def load(self, file_id: str) -> bytes:
        pass

    @abstractmethod
    async def delete(self, file_id: str) -> None:
        pass