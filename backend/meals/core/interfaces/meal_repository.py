from abc import ABC, abstractmethod
from meals.core.entities.meal import Meal


class IMealRepository(ABC):
    @abstractmethod
    async def get_by_id(self, meal_id: str) -> Meal:
        pass

    @abstractmethod
    async def update(
            self,
            meal_id: str,
            title: str,
            description: str | None,
    ) -> Meal:
        pass

    @abstractmethod
    async def set_photo_path(self, meal_id: str, photo_path: str) -> None:
        pass

    @abstractmethod
    async def set_active_status(self, meal_id: str, is_active: bool) -> Meal:
        pass

    @abstractmethod
    async def get_all(self) -> list[Meal]:
        pass