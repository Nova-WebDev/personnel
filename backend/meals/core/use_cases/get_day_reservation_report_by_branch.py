from datetime import date

from meals.core.entities.day_reservation_report import DayReservationReportByBranch
from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.voucher_repository import IVoucherRepository
from user.core.entities.permission_level import PermissionLevel


class GetDayReservationReportByBranch:
    def __init__(self, voucher_repository: IVoucherRepository):
        self.voucher_repository = voucher_repository

    async def execute(self, plan_date: date, permissions: list[dict]) -> DayReservationReportByBranch:
        self._authorize(permissions)
        return await self.voucher_repository.get_day_report_by_branch(plan_date)

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        allowed = {PermissionLevel.ADMIN.value, PermissionLevel.KITCHEN.value}

        if not any(p["level"] in allowed for p in permissions):
            raise PermissionDeniedError()