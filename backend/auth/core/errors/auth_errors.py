class InvalidPhoneFormatError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserBlockedError(Exception):
    pass

class PhoneTemporarilyBlockedError(Exception):
    pass

class InvalidVerificationCodeError(Exception):
    pass

class InvalidRefreshToken(Exception):
    pass