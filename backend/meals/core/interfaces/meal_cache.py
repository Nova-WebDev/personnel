from abc import ABC, abstractmethod


class IMealCache(ABC):
    @abstractmethod
    async def set(self, meal_id: str, data: str) -> None:
        pass

    @abstractmethod
    async def get(self, meal_id: str) -> str | None:
        pass

    @abstractmethod
    async def get_all(self) -> dict[str, str]:
        pass

    @abstractmethod
    async def delete(self, meal_id: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass