from app.utils.errors import DomainError


class BranchNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Branch not found"):
        super().__init__(message)


class PermissionDeniedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Admin permission required"):
        super().__init__(message)


class UnitNameConflictError(DomainError):
    status_code = 409

    def __init__(self, message: str = "A unit with this name already exists in this branch"):
        super().__init__(message)


class UnitNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Unit not found"):
        super().__init__(message)


class PhoneConflictError(DomainError):
    status_code = 409

    def __init__(self, message: str = "A user with this phone number already exists"):
        super().__init__(message)


class PersonnelCodeConflictError(DomainError):
    status_code = 409

    def __init__(self, message: str = "A user with this personnel code already exists"):
        super().__init__(message)


class UserNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class PhotoNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Photo not found"):
        super().__init__(message)