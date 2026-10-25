from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from meals.core.interfaces.report_repository import IReportRepository

from meals.infrastructure.data.models.meal_plan import MealPlanModel

from meals.infrastructure.data.models.meal import MealModel
from meals.infrastructure.data.models.guest_reservation import GuestReservationModel
from meals.infrastructure.data.models.voucher import VoucherModel

from user.infrastructure.data.models.branch import BranchModel
from user.infrastructure.data.models.user import UserModel
from user.infrastructure.data.models.unit import UnitModel




class ReportRepository(IReportRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def count_active_users(self) -> int:
        stmt = select(func.count(UserModel.id)).where(UserModel.is_blocked.is_(False))
        return await self._scalar(stmt)

    async def count_active_meals(self) -> int:
        stmt = select(func.count(MealModel.id)).where(MealModel.is_active.is_(True))
        return await self._scalar(stmt)

    async def count_branches(self) -> int:
        stmt = select(func.count(BranchModel.id))
        return await self._scalar(stmt)

    async def _scalar(self, stmt) -> int:
        return int((await self._session.execute(stmt)).scalar_one())


    async def get_guest_totals(self, date_from: date, date_to: date) -> tuple[int, int]:
        days_stmt = (
            select(func.count(func.distinct(MealPlanModel.plan_date)))
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                MealPlanModel.plan_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
        )
        guests_stmt = (
            select(func.coalesce(func.sum(GuestReservationModel.guest_count), 0))
            .join(MealPlanModel, MealPlanModel.id == GuestReservationModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                GuestReservationModel.reservation_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
        )

        days = await self._scalar(days_stmt)
        guests = await self._scalar(guests_stmt)

        return guests, days


    async def get_daily_meal_counts(self, date_from: date, date_to: date) -> dict[date, int]:
        voucher_stmt = (
            select(VoucherModel.reservation_date, func.count(VoucherModel.id))
            .join(MealPlanModel, MealPlanModel.id == VoucherModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                VoucherModel.reservation_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
            .group_by(VoucherModel.reservation_date)
        )
        guest_stmt = (
            select(GuestReservationModel.reservation_date, func.sum(GuestReservationModel.guest_count))
            .join(MealPlanModel, MealPlanModel.id == GuestReservationModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                GuestReservationModel.reservation_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
            .group_by(GuestReservationModel.reservation_date)
        )

        counts: dict[date, int] = {}
        for stmt in (voucher_stmt, guest_stmt):
            for day, total in (await self._session.execute(stmt)).all():
                counts[day] = counts.get(day, 0) + int(total)

        return counts

    async def get_branch_usage(self, date_from: date, date_to: date) -> list[dict]:
        branches = (
            await self._session.execute(
                select(BranchModel.id, BranchModel.name).order_by(BranchModel.name)
            )
        ).all()

        voucher_stmt = (
            select(
                UnitModel.branch_id,
                func.count(case((VoucherModel.is_used.is_(True), 1))),
                func.count(case((VoucherModel.is_used.is_(False), 1))),
            )
            .select_from(VoucherModel)
            .join(UserModel, UserModel.id == VoucherModel.user_id)
            .join(UnitModel, UnitModel.id == UserModel.unit_id)
            .join(MealPlanModel, MealPlanModel.id == VoucherModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                VoucherModel.reservation_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
            .group_by(UnitModel.branch_id)
        )
        guest_stmt = (
            select(
                UnitModel.branch_id,
                func.coalesce(func.sum(
                    case((GuestReservationModel.is_used.is_(True), GuestReservationModel.guest_count), else_=0)), 0),
                func.coalesce(func.sum(
                    case((GuestReservationModel.is_used.is_(False), GuestReservationModel.guest_count), else_=0)), 0),
            )
            .select_from(GuestReservationModel)
            .join(UnitModel, UnitModel.id == GuestReservationModel.unit_id)
            .join(MealPlanModel, MealPlanModel.id == GuestReservationModel.meal_plan_id)
            .join(MealModel, MealModel.id == MealPlanModel.meal_id)
            .where(
                GuestReservationModel.reservation_date.between(date_from, date_to),
                MealModel.is_active.is_(True),
            )
            .group_by(UnitModel.branch_id)
        )

        totals: dict[str, dict[str, int]] = {
            branch_id: {"used": 0, "unused": 0} for branch_id, _ in branches
        }
        for stmt in (voucher_stmt, guest_stmt):
            for branch_id, used, unused in (await self._session.execute(stmt)).all():
                totals[branch_id]["used"] += int(used)
                totals[branch_id]["unused"] += int(unused)

        return [
            {
                "branch_id": branch_id,
                "branch_name": name,
                "used": totals[branch_id]["used"],
                "unused": totals[branch_id]["unused"],
            }
            for branch_id, name in branches
        ]