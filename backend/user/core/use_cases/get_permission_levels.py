from user.core.entities.permission_level import PermissionLevel, SCOPED_PERMISSION_LEVELS
from user.core.entities.permission_level_info import PermissionLevelInfo
from user.core.errors.user_errors import PermissionDeniedError


class GetPermissionLevels:
    async def execute(self, permissions: list[dict]) -> list[PermissionLevelInfo]:
        self._authorize(permissions)

        return [
            PermissionLevelInfo(
                level=level.value,
                requires_scope=level in SCOPED_PERMISSION_LEVELS,
            )
            for level in PermissionLevel
        ]

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)

        if not is_admin:
            raise PermissionDeniedError()