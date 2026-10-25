from datetime import datetime, timedelta, timezone

from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.report_repository import IReportRepository
from user.core.entities.permission_level import PermissionLevel

WINDOW_DAYS = 30


class GetAverageGuests:
    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, permissions: list[dict]) -> float:
        self._authorize(permissions)

        today = datetime.now(timezone.utc).date()
        date_from = today - timedelta(days=WINDOW_DAYS - 1)

        total_guests, plan_days = await self.report_repository.get_guest_totals(date_from, today)

        if plan_days == 0:
            return 0.0

        return round(total_guests / plan_days, 1)

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()