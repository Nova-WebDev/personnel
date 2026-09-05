import secrets
from auth.core.interfaces.generat_token import IGenerator


class SecureTokenGenerator(IGenerator):
    def __init__(self, length: int = 32):
        self.length = length

    def generate(self) -> str:
        return secrets.token_urlsafe(self.length)
