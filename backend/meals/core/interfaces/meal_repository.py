from abc import ABC, abstractmethod
from meals.core.entities.meal import Meal


class IMealRepository(ABC):
    @abstractmethod
    async def create(
        self,
        meal_id: str,
        title: str,
        description: str | None,
        photo_path: str | None,
    ) -> Meal:
        pass