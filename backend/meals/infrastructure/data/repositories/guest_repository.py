import uuid
from datetime import date

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.inviter_guest_row import InviterGuestRow
from meals.core.entities.meal import Meal
from meals.core.errors.meals_errors import MealPlanNotFoundError
from meals.core.interfaces.guest_repository import IGuestRepository
from meals.infrastructure.data.models.guest_reservation import GuestReservationModel
from meals.infrastructure.data.models.meal import MealModel
from meals.infrastructure.data.models.meal_plan import MealPlanModel
from user.core.errors.user_errors import UnitNotFoundError


class GuestRepository(IGuestRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_plan_context(self, meal_plan_id: str) -> tuple[date, bool]:
        row = (
            await self._session.execute(
                select(MealPlanModel.plan_date, MealModel.is_active)
                .join(MealModel, MealModel.id == MealPlanModel.meal_id)
                .where(MealPlanModel.id == meal_plan_id)
            )
        ).one_or_none()

        if row is None:
            raise MealPlanNotFoundError()

        return row[0], row[1]

    async def set_guest_count(
        self, meal_plan_id: str, unit_id: str, invited_by: str, plan_date: date, guest_count: int
    ) -> int:
        if guest_count == 0:
            await self._session.execute(
                delete(GuestReservationModel).where(
                    GuestReservationModel.meal_plan_id == meal_plan_id,
                    GuestReservationModel.unit_id == unit_id,
                    GuestReservationModel.invited_by == invited_by,
                )
            )
        else:
            insert_stmt = pg_insert(GuestReservationModel).values(
                id=str(uuid.uuid4()),
                meal_plan_id=meal_plan_id,
                unit_id=unit_id,
                invited_by=invited_by,
                guest_count=guest_count,
                reservation_date=plan_date,
            )
            stmt = insert_stmt.on_conflict_do_update(
                constraint="uq_guest_plan_unit_inviter",
                set_={"guest_count": guest_count},
            )

            try:
                async with self._session.begin_nested():
                    await self._session.execute(stmt)
            except IntegrityError:
                raise UnitNotFoundError()

        total = await self._session.execute(
            select(func.coalesce(func.sum(GuestReservationModel.guest_count), 0)).where(
                GuestReservationModel.meal_plan_id == meal_plan_id,
                GuestReservationModel.unit_id == unit_id,
            )
        )
        return int(total.scalar_one())

    async def get_inviter_guests(self, user_id: str, day: date) -> list[InviterGuestRow]:
        stmt = (
            select(
                GuestReservationModel.meal_plan_id,
                GuestReservationModel.guest_count,
                GuestReservationModel.is_used,
                MealModel.id,
                MealModel.title,
                MealModel.description,
                MealModel.photo_path,
                MealModel.is_active,
            )
            .join(MealPlanModel, MealPlanModel.id == GuestReservationModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                GuestReservationModel.invited_by == user_id,
                GuestReservationModel.reservation_date == day,
                MealModel.is_active.is_(True),
            )
        )
        rows = (await self._session.execute(stmt)).all()

        return [
            InviterGuestRow(
                meal_plan_id=row[0],
                guest_count=row[1],
                is_used=row[2],
                meal=Meal(id=row[3], title=row[4], description=row[5], photo_path=row[6], is_active=row[7]),
            )
            for row in rows
        ]

    async def mark_inviter_guests_used(self, user_id: str, day: date) -> dict[str, int]:
        active_plan_ids = (
            select(MealPlanModel.id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(MealModel.is_active.is_(True))
        )
        stmt = (
            update(GuestReservationModel)
            .where(
                GuestReservationModel.invited_by == user_id,
                GuestReservationModel.reservation_date == day,
                GuestReservationModel.is_used.is_(False),
                GuestReservationModel.meal_plan_id.in_(active_plan_ids),
            )
            .values(is_used=True)
            .returning(GuestReservationModel.meal_plan_id, GuestReservationModel.guest_count)
        )

        delivered: dict[str, int] = {}
        for meal_plan_id, guest_count in (await self._session.execute(stmt)).all():
            delivered[meal_plan_id] = delivered.get(meal_plan_id, 0) + guest_count

        return delivered