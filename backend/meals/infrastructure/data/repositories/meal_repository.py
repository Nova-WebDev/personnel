from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.entities.meal import Meal
from meals.core.errors.meals_errors import MealNotFoundError
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

    async def get_by_id(self, meal_id: str) -> Meal:
        model = await self._session.get(MealModel, meal_id)

        if model is None:
            raise MealNotFoundError()

        return Meal(
            id=model.id,
            title=model.title,
            description=model.description,
            photo_path=model.photo_path,
            is_active=model.is_active,
        )

    async def update(
        self,
        meal_id: str,
        title: str,
        description: str | None,
    ) -> Meal:
        model = await self._session.get(MealModel, meal_id)

        if model is None:
            raise MealNotFoundError()

        model.title = title
        model.description = description

        await self._session.flush()
        await self._session.refresh(model)

        return Meal(
            id=model.id,
            title=model.title,
            description=model.description,
            photo_path=model.photo_path,
            is_active=model.is_active,
        )

    async def set_photo_path(self, meal_id: str, photo_path: str) -> None:
        stmt = update(MealModel).where(MealModel.id == meal_id).values(photo_path=photo_path)
        await self._session.execute(stmt)
        await self._session.flush()

    async def set_active_status(self, meal_id: str, is_active: bool) -> Meal:
        stmt = update(MealModel).where(MealModel.id == meal_id).values(is_active=is_active)
        await self._session.execute(stmt)
        await self._session.flush()

        return await self.get_by_id(meal_id)

    async def get_all(self) -> list[Meal]:
        stmt = select(MealModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [
            Meal(
                id=m.id,
                title=m.title,
                description=m.description,
                photo_path=m.photo_path,
                is_active=m.is_active,
            )
            for m in models
        ]