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

class PersonnelIdAlreadyExistsError(DomainError):
    status_code = 409

    def __init__(self, message: str = "Personnel with this personnel_id already exists"):
        super().__init__(message)

class PersonnelNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "Personnel not found"):
        super().__init__(message)

class InvalidPhotoFileError(DomainError):
    status_code = 400

    def __init__(self, message: str = "Invalid image file"):
        super().__init__(message)

class QRCodeRateLimitedError(DomainError):
    status_code = 429

    def __init__(self, message: str = "Please wait before requesting the QR code again"):
        super().__init__(message)

        
class TooManyRequestsError(DomainError):
    status_code = 429

    def __init__(self, message: str = "Too many requests, please try again later"):
        super().__init__(message)