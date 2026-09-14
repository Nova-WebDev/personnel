import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.interfaces.meal_plan_time_policy_repository import IMealPlanTimePolicyRepository
from meals.core.entities.meal_plan_time_policy import MealPlanTimePolicy
from meals.core.entities.week_day import WeekDay
from meals.infrastructure.data.models.meal_plan_time_policy import MealPlanTimePolicyModel


class MealPlanTimePolicyRepository(IMealPlanTimePolicyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_all(self, policies: list[dict]) -> list[MealPlanTimePolicy]:
        stmt = select(MealPlanTimePolicyModel)
        result = await self._session.execute(stmt)
        existing = {m.target_weekday: m for m in result.scalars().all()}

        models = []
        for p in policies:
            weekday = WeekDay(p["target_weekday"])

            if weekday in existing:
                model = existing[weekday]
                model.cutoff_hours_before = p["cutoff_hours_before"]
            else:
                model = MealPlanTimePolicyModel(
                    id=str(uuid.uuid4()),
                    target_weekday=weekday,
                    cutoff_hours_before=p["cutoff_hours_before"],
                )
                self._session.add(model)

            models.append(model)

        await self._session.flush()

        return [
            MealPlanTimePolicy(
                id=m.id,
                target_weekday=m.target_weekday,
                cutoff_hours_before=m.cutoff_hours_before,
            )
            for m in models
        ]

    async def get_all(self) -> list[MealPlanTimePolicy]:
        stmt = select(MealPlanTimePolicyModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [
            MealPlanTimePolicy(
                id=m.id,
                target_weekday=m.target_weekday,
                cutoff_hours_before=m.cutoff_hours_before,
            )
            for m in models
        ]