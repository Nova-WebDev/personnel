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


class InvalidRecurringCycleError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Recurring cycle is invalid"):
        super().__init__(message)


class UserBlockedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "Blocked users cannot reserve meals"):
        super().__init__(message)


class VoucherAlreadyUsedError(DomainError):
    status_code = 409

    def __init__(self, message: str = "A used reservation cannot be changed"):
        super().__init__(message)


class ReservationDeadlinePassedError(DomainError):
    status_code = 409

    def __init__(self, message: str = "The reservation deadline for this date has passed"):
        super().__init__(message)


class VoucherNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Reservation not found"):
        super().__init__(message)

class InvalidBulkReservationError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Invalid bulk reservation request"):
        super().__init__(message)


class UserOutOfScopeError(DomainError):
    status_code = 403

    def __init__(self, message: str = "One or more users are not in your units"):
        super().__init__(message)


class RfidCardNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "No user is registered with this RFID card"):
        super().__init__(message)


class InvalidGuestCountError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Guest count must be between 0 and 50"):
        super().__init__(message)