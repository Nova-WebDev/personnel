from app.utils.errors import DomainError


class PermissionDeniedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Admin permission required"):
        super().__init__(message)


class InvalidTimePolicyError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Time policy must include all seven weekdays exactly once"):
        super().__init__(message)
