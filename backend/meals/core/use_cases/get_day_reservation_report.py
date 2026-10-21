from datetime import date

from meals.core.entities.day_reservation_report import DayReservationReport
from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.voucher_repository import IVoucherRepository
from user.core.entities.permission_level import PermissionLevel


class GetDayReservationReport:
    def __init__(self, voucher_repository: IVoucherRepository):
        self.voucher_repository = voucher_repository

    async def execute(self, plan_date: date, permissions: list[dict]) -> DayReservationReport:
        unit_ids = self._resolve_units(permissions)
        return await self.voucher_repository.get_day_report(plan_date, unit_ids)

    @staticmethod
    def _resolve_units(permissions: list[dict]) -> list[str] | None:
        if any(p["scope"] is None for p in permissions):
            return None

        unit_ids = list(
            {
                p["scope"]
                for p in permissions
                if p["level"] == PermissionLevel.GROUP_MANAGER.value
            }
        )

        if not unit_ids:
            raise PermissionDeniedError()

        return unit_ids