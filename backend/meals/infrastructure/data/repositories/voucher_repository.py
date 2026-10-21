import uuid
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from meals.core.entities.cancellation_context import CancellationContext
from meals.core.entities.day_reservation_report import (
    BranchInfo,
    BranchUnits,
    DayMealPlan,
    DayReservationReport,
    DayReservationReportByBranch,
    MemberInfo,
    UnitInfo,
    UnitMembers,
)
from meals.core.entities.meal import Meal
from meals.core.entities.reservation_context import ReservationContext
from meals.core.entities.voucher_summary import VoucherSummary
from meals.core.errors.meals_errors import MealPlanNotFoundError
from meals.core.interfaces.voucher_repository import IVoucherRepository
from meals.infrastructure.data.models.meal import MealModel
from meals.infrastructure.data.models.meal_plan import MealPlanModel
from meals.infrastructure.data.models.voucher import VoucherModel
from user.core.errors.user_errors import UserNotFoundError
from user.infrastructure.data.models.branch import BranchModel
from user.infrastructure.data.models.unit import UnitModel
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

    async def get_day_report(self, plan_date: date, unit_ids: list[str] | None) -> DayReservationReport:
        plan_rows = (
            await self._session.execute(
                select(
                    MealPlanModel.id,
                    MealModel.id,
                    MealModel.title,
                    MealModel.description,
                    MealModel.photo_path,
                    MealModel.is_active,
                )
                .join(MealModel, MealModel.id == MealPlanModel.meal_id)
                .where(
                    MealPlanModel.plan_date == plan_date,
                    MealModel.is_active.is_(True),
                )
                .order_by(MealModel.title)
            )
        ).all()

        meals_by_plan = {
            row[0]: Meal(id=row[1], title=row[2], description=row[3], photo_path=row[4], is_active=row[5])
            for row in plan_rows
        }

        member_stmt = (
            select(
                UserModel.id,
                UserModel.phone,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.personnel_code,
                UserModel.rfid_card_id,
                UserModel.photo_path,
                UserModel.is_blocked,
                UnitModel.id,
                UnitModel.name,
                BranchModel.id,
                BranchModel.name,
                VoucherModel.meal_plan_id,
                VoucherModel.is_used,
            )
            .select_from(UserModel)
            .join(UnitModel, UnitModel.id == UserModel.unit_id)
            .join(BranchModel, BranchModel.id == UnitModel.branch_id)
            .outerjoin(
                VoucherModel,
                (VoucherModel.user_id == UserModel.id) & (VoucherModel.reservation_date == plan_date),
            )
            .order_by(UnitModel.name, UserModel.last_name, UserModel.first_name)
        )
        if unit_ids is not None:
            member_stmt = member_stmt.where(UserModel.unit_id.in_(unit_ids))

        member_rows = (await self._session.execute(member_stmt)).all()

        units: dict[str, UnitMembers] = {}
        for row in member_rows:
            unit = units.setdefault(
                row[8],
                UnitMembers(unit=UnitInfo(id=row[8], name=row[9], branch_id=row[10], branch_name=row[11])),
            )

            meal = meals_by_plan.get(row[12])
            is_reserved = meal is not None

            unit.members.append(
                MemberInfo(
                    id=row[0],
                    phone=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    personnel_code=row[4],
                    rfid_card_id=row[5],
                    photo_path=row[6],
                    is_blocked=row[7],
                    is_reserved=is_reserved,
                    meal_plan_id=row[12] if is_reserved else None,
                    meal=meal,
                    is_used=row[13] if is_reserved else None,
                )
            )

        return DayReservationReport(
            plan_date=plan_date,
            meal_plans=[
                DayMealPlan(meal_plan_id=plan_id, meal=meal)
                for plan_id, meal in meals_by_plan.items()
            ],
            units=list(units.values()),
        )

    async def get_day_report_by_branch(self, plan_date: date) -> DayReservationReportByBranch:
        report = await self.get_day_report(plan_date, None)

        branches: dict[str, BranchUnits] = {}
        for unit_members in report.units:
            unit = unit_members.unit
            branch = branches.setdefault(
                unit.branch_id,
                BranchUnits(branch=BranchInfo(id=unit.branch_id, name=unit.branch_name)),
            )
            branch.units.append(unit_members)

        return DayReservationReportByBranch(
            plan_date=plan_date,
            meal_plans=report.meal_plans,
            branches=sorted(branches.values(), key=lambda b: b.branch.name),
        )