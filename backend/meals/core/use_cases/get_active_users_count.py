from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.report_repository import IReportRepository
from user.core.entities.permission_level import PermissionLevel


class GetActiveUsersCount:
    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, permissions: list[dict]) -> int:
        self._authorize(permissions)
        return await self.report_repository.count_active_users()

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()