import enum

class PermissionLevel(str, enum.Enum):
    ADMIN = "admin"
    KITCHEN = "kitchen"
    GROUP_MANAGER = "group_manager"
    HR_MANAGER = "hr_manager"


SCOPED_PERMISSION_LEVELS = frozenset({
    PermissionLevel.GROUP_MANAGER,
    PermissionLevel.HR_MANAGER,
})