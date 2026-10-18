import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.meal_plan_recurring import MealPlanRecurring
from meals.core.interfaces.meal_plan_recurring_repository import IMealPlanRecurringRepository
from meals.infrastructure.data.models.meal_plan_recurring import MealPlanRecurringModel


class MealPlanRecurringRepository(IMealPlanRecurringRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def replace_all(self, items: list[dict]) -> list[MealPlanRecurring]:
        await self._session.execute(delete(MealPlanRecurringModel))

        models = [
            MealPlanRecurringModel(
                id=str(uuid.uuid4()),
                target_date=i["target_date"],
                meal_id=i["meal_id"],
            )
            for i in items
        ]
        self._session.add_all(models)
        await self._session.flush()

        return [
            MealPlanRecurring(id=m.id, target_date=m.target_date, meal_id=m.meal_id)
            for m in models
        ]

    async def get_all(self) -> list[MealPlanRecurring]:
        stmt = select(MealPlanRecurringModel).order_by(MealPlanRecurringModel.target_date)
        result = await self._session.execute(stmt)

        return [
            MealPlanRecurring(id=m.id, target_date=m.target_date, meal_id=m.meal_id)
            for m in result.scalars().all()
        ]