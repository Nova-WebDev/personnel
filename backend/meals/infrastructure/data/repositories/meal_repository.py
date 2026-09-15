from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.entities.meal import Meal
from meals.infrastructure.data.models.meal import MealModel


class MealRepository(IMealRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        meal_id: str,
        title: str,
        description: str | None,
        photo_path: str | None,
    ) -> Meal:
        model = MealModel(
            id=meal_id,
            title=title,
            description=description,
            photo_path=photo_path,
            is_active=True,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)

        return Meal(
            id=model.id,
            title=model.title,
            description=model.description,
            photo_path=model.photo_path,
            is_active=model.is_active,
        )