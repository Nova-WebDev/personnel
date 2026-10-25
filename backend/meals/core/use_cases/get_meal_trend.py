from datetime import datetime, timedelta, timezone

from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.report_repository import IReportRepository
from user.core.entities.permission_level import PermissionLevel

WINDOW_DAYS = 30


class GetMealTrend:
    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, permissions: list[dict]) -> list[dict]:
        self._authorize(permissions)

        today = datetime.now(timezone.utc).date()
        date_from = today - timedelta(days=WINDOW_DAYS - 1)

        counts = await self.report_repository.get_daily_meal_counts(date_from, today)

        return [
            {"date": day, "count": counts.get(day, 0)}
            for day in (date_from + timedelta(days=i) for i in range(WINDOW_DAYS))
        ]

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()