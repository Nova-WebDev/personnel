class DomainError(Exception):
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)


class InvalidPhoneFormatError(DomainError):
    status_code = 400

    def __init__(self, message: str = "Invalid phone number format"):
        super().__init__(message)


class UserNotFoundError(DomainError):
    status_code = 404

    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class UserBlockedError(DomainError):
    status_code = 403

    def __init__(self, message: str = "User is blocked"):
        super().__init__(message)


class PhoneTemporarilyBlockedError(DomainError):
    status_code = 429

    def __init__(self, message: str = "Phone number is temporarily blocked"):
        super().__init__(message)


class InvalidVerificationCodeError(DomainError):
    status_code = 400

    def __init__(self, message: str = "Invalid verification code"):
        super().__init__(message)


class InvalidRefreshToken(DomainError):
    status_code = 401

    def __init__(self, message: str = "Invalid or expired refresh token"):
        super().__init__(message)