import uuid
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.reservation_context import ReservationContext
from meals.core.entities.voucher_summary import VoucherSummary
from meals.core.entities.cancellation_context import CancellationContext

from meals.core.errors.meals_errors import MealPlanNotFoundError
from user.core.errors.user_errors import UserNotFoundError

from meals.core.interfaces.voucher_repository import IVoucherRepository

from meals.infrastructure.data.models.meal import MealModel
from meals.infrastructure.data.models.meal_plan import MealPlanModel
from meals.infrastructure.data.models.voucher import VoucherModel
from user.infrastructure.data.models.user import UserModel


class VoucherRepository(IVoucherRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_reservation_context(self, user_id: str, meal_plan_id: str) -> ReservationContext:
        plan_row = (
            await self._session.execute(
                select(MealPlanModel.plan_date, MealModel.is_active)
                .join(MealModel, MealModel.id == MealPlanModel.meal_id)
                .where(MealPlanModel.id == meal_plan_id)
            )
        ).one_or_none()

        if plan_row is None:
            raise MealPlanNotFoundError()

        plan_date, meal_is_active = plan_row

        stmt = (
            select(
                UserModel.is_blocked,
                UserModel.unit_id,
                VoucherModel.id,
                VoucherModel.meal_plan_id,
                VoucherModel.is_used,
            )
            .select_from(UserModel)
            .outerjoin(
                VoucherModel,
                (VoucherModel.user_id == UserModel.id) & (VoucherModel.reservation_date == plan_date),
            )
            .where(UserModel.id == user_id)
        )
        row = (await self._session.execute(stmt)).one_or_none()

        if row is None:
            raise UserNotFoundError()

        return ReservationContext(
            plan_date=plan_date,
            meal_is_active=meal_is_active,
            user_is_blocked=row[0],
            user_unit_id=row[1],
            current_voucher_id=row[2],
            current_meal_plan_id=row[3],
            current_is_used=row[4],
        )

    async def upsert_reservation(
        self, user_id: str, meal_plan_id: str, reservation_date: date
    ) -> VoucherSummary | None:
        insert_stmt = pg_insert(VoucherModel).values(
            id=str(uuid.uuid4()),
            user_id=user_id,
            meal_plan_id=meal_plan_id,
            reservation_date=reservation_date,
            is_used=False,
        )
        stmt = insert_stmt.on_conflict_do_update(
            constraint="uq_voucher_user_date",
            set_={"meal_plan_id": meal_plan_id},
            where=VoucherModel.is_used.is_(False),
        ).returning(
            VoucherModel.id,
            VoucherModel.user_id,
            VoucherModel.meal_plan_id,
            VoucherModel.reservation_date,
        )
        row = (await self._session.execute(stmt)).one_or_none()

        if row is None:
            return None

        return VoucherSummary(id=row[0], user_id=row[1], meal_plan_id=row[2], reservation_date=row[3])



    async def get_cancellation_context(self, user_id: str, meal_plan_id: str) -> CancellationContext:
        stmt = (
            select(MealPlanModel.plan_date, UserModel.unit_id)
            .select_from(MealPlanModel)
            .join(UserModel, UserModel.id == user_id)
            .where(MealPlanModel.id == meal_plan_id)
        )
        row = (await self._session.execute(stmt)).one_or_none()

        if row is None:
            raise MealPlanNotFoundError()

        return CancellationContext(plan_date=row[0], user_unit_id=row[1])

    async def delete_unused(self, user_id: str, meal_plan_id: str) -> bool:
        stmt = (
            delete(VoucherModel)
            .where(
                VoucherModel.user_id == user_id,
                VoucherModel.meal_plan_id == meal_plan_id,
                VoucherModel.is_used.is_(False),
            )
            .returning(VoucherModel.id)
        )
        return (await self._session.execute(stmt)).scalar_one_or_none() is not None

    async def is_used(self, user_id: str, meal_plan_id: str) -> bool | None:
        stmt = select(VoucherModel.is_used).where(
            VoucherModel.user_id == user_id,
            VoucherModel.meal_plan_id == meal_plan_id,
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()