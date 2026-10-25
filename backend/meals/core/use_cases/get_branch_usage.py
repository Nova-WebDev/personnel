from datetime import datetime, timedelta, timezone

from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.report_repository import IReportRepository
from user.core.entities.permission_level import PermissionLevel

WINDOW_DAYS = 365


class GetBranchUsage:
    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, permissions: list[dict]) -> list[dict]:
        self._authorize(permissions)

        today = datetime.now(timezone.utc).date()
        date_from = today - timedelta(days=WINDOW_DAYS - 1)

        return await self.report_repository.get_branch_usage(date_from, today)

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()