from app.utils.errors import DomainError


class PermissionDeniedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Admin permission required"):
        super().__init__(message)


class InvalidTimePolicyError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Time policy must include all seven weekdays exactly once"):
        super().__init__(message)


class MealNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Meal not found"):
        super().__init__(message)

class MealNotActiveError(DomainError):
    status_code = 409

    def __init__(self, message: str = "Meal is not active"):
        super().__init__(message)


class MealPlanAlreadyExistsError(DomainError):
    status_code = 409

    def __init__(self, message: str = "This meal is already planned for this date"):
        super().__init__(message)


class MealPlanDeadlinePassedError(DomainError):
    status_code = 409

    def __init__(self, message: str = "The deadline for planning this date has passed"):
        super().__init__(message)


class MealPlanNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Meal plan not found"):
        super().__init__(message)

class InvalidDateRangeError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Invalid date range"):
        super().__init__(message)


class MealPhotoNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Meal photo not found"):
        super().__init__(message)