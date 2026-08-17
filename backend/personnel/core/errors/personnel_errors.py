from auth.core.errors.auth_errors import DomainError


class BranchAlreadyExistsError(DomainError):
    status_code = 409

    def __init__(self, message: str = "Branch with this name already exists"):
        super().__init__(message)

class BranchNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Branch not found"):
        super().__init__(message)

class UnitAlreadyExistsError(DomainError):
    status_code = 409

    def __init__(self, message: str = "Unit with this name already exists in this branch"):
        super().__init__(message)

class UnitNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Unit not found"):
        super().__init__(message)