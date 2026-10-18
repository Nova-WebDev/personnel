import uuid
from datetime import date

from sqlalchemy import Date, cast, literal, select, update, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.meal import Meal
from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal
from meals.core.errors.meals_errors import (
    MealNotActiveError,
    MealNotFoundError,
    MealPlanAlreadyExistsError,
    MealPlanNotFoundError,
)
from meals.core.interfaces.meal_plan_repository import IMealPlanRepository
from meals.infrastructure.data.models.meal import MealModel
from meals.infrastructure.data.models.meal_plan import MealPlanModel


class MealPlanRepository(IMealPlanRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_for_active_meal(self, plan_date: date, meal_id: str) -> MealPlanWithMeal:
        meal_plan_id = str(uuid.uuid4())

        active_meal = select(
            literal(meal_plan_id),
            cast(literal(plan_date), Date),
            MealModel.id,
        ).where(MealModel.id == meal_id, MealModel.is_active.is_(True))

        inserted = (
            pg_insert(MealPlanModel)
            .from_select(["id", "plan_date", "meal_id"], active_meal)
            .on_conflict_do_nothing(constraint="uq_mealplan_date_meal")
            .returning(MealPlanModel.id, MealPlanModel.meal_id)
            .cte("inserted")
        )

        stmt = select(
            inserted.c.id,
            MealModel.id,
            MealModel.title,
            MealModel.description,
            MealModel.photo_path,
            MealModel.is_active,
        ).join(MealModel, MealModel.id == inserted.c.meal_id)

        result = await self._session.execute(stmt)
        row = result.one_or_none()

        if row is None:
            await self._raise_failure_reason(meal_id)

        return self._to_entity(row[0], plan_date, row[1:])

    async def get_plan_date(self, meal_plan_id: str) -> date:
        stmt = select(MealPlanModel.plan_date).where(MealPlanModel.id == meal_plan_id)
        result = await self._session.execute(stmt)
        plan_date = result.scalar_one_or_none()

        if plan_date is None:
            raise MealPlanNotFoundError()

        return plan_date

    async def change_meal(self, meal_plan_id: str, meal_id: str) -> MealPlanWithMeal:
        active_meal_id = (
            select(MealModel.id)
            .where(MealModel.id == meal_id, MealModel.is_active.is_(True))
            .scalar_subquery()
        )

        updated = (
            update(MealPlanModel)
            .where(MealPlanModel.id == meal_plan_id)
            .values(meal_id=active_meal_id)
            .returning(MealPlanModel.id, MealPlanModel.plan_date, MealPlanModel.meal_id)
            .cte("updated")
        )

        stmt = select(
            updated.c.id,
            updated.c.plan_date,
            MealModel.id,
            MealModel.title,
            MealModel.description,
            MealModel.photo_path,
            MealModel.is_active,
        ).join(MealModel, MealModel.id == updated.c.meal_id)

        try:
            async with self._session.begin_nested():
                result = await self._session.execute(stmt)
        except IntegrityError:
            await self._raise_failure_reason(meal_id)

        row = result.one()

        return self._to_entity(row[0], row[1], row[2:])

    async def _raise_failure_reason(self, meal_id: str) -> None:
        meal = await self._session.get(MealModel, meal_id)

        if meal is None:
            raise MealNotFoundError()
        if not meal.is_active:
            raise MealNotActiveError()

        raise MealPlanAlreadyExistsError()

    @staticmethod
    def _to_entity(meal_plan_id: str, plan_date: date, meal_row) -> MealPlanWithMeal:
        meal_id, title, description, photo_path, is_active = meal_row

        return MealPlanWithMeal(
            id=meal_plan_id,
            plan_date=plan_date,
            meal=Meal(
                id=meal_id,
                title=title,
                description=description,
                photo_path=photo_path,
                is_active=is_active,
            ),
        )

    async def delete(self, meal_plan_id: str) -> None:
        stmt = delete(MealPlanModel).where(MealPlanModel.id == meal_plan_id).returning(MealPlanModel.id)
        result = await self._session.execute(stmt)

        if result.scalar_one_or_none() is None:
            raise MealPlanNotFoundError()