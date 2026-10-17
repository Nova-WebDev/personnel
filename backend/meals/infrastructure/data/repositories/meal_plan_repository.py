import uuid
from datetime import date

from sqlalchemy import Date, cast, literal, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.meal import Meal
from meals.core.entities.meal_plan_with_meal import MealPlanWithMeal
from meals.core.errors.meals_errors import (
    MealNotActiveError,
    MealNotFoundError,
    MealPlanAlreadyExistsError,
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

        return MealPlanWithMeal(
            id=row[0],
            plan_date=plan_date,
            meal=Meal(
                id=row[1],
                title=row[2],
                description=row[3],
                photo_path=row[4],
                is_active=row[5],
            ),
        )

    async def _raise_failure_reason(self, meal_id: str) -> None:
        meal = await self._session.get(MealModel, meal_id)

        if meal is None:
            raise MealNotFoundError()
        if not meal.is_active:
            raise MealNotActiveError()

        raise MealPlanAlreadyExistsError()