class DomainError(Exception):
    status_code: int = 500

    def __init__(self, message: str = "Internal error"):
        super().__init__(message)

class InvalidPhotoFileError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Invalid or unsupported photo file"):
        super().__init__(message)