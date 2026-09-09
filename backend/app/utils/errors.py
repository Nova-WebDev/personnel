class DomainError(Exception):
    status_code: int = 500

    def __init__(self, message: str = "Internal error"):
        super().__init__(message)

class InvalidPhotoFileError(DomainError):
    status_code = 422

    def __init__(self, message: str = "Invalid or unsupported photo file"):
        super().__init__(message)

class TooManyRequestsError(DomainError):
    status_code = 429

    def __init__(self, message: str = "Too many requests"):
        super().__init__(message)


class InvalidApiKeyError(DomainError):
    status_code = 401

    def __init__(self, message: str = "Invalid API key"):
        super().__init__(message)