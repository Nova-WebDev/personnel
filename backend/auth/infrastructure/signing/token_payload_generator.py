from auth.core.entities.token_payload import TokenPayload
from auth.core.interfaces.token_payload_generator import ITokenPayloadGenerator


class TokenPayloadGenerator(ITokenPayloadGenerator):
    def __init__(self, expires_in_seconds: int = 15 * 60):
        self.expires_in = expires_in_seconds

    async def generate_payload(self, base: dict) -> TokenPayload:
        iat = base["iat"]
        exp = iat + self.expires_in
        return TokenPayload(
            id=base["id"],
            phone_number=base["phone_number"],
            permissions=base["permissions"],
            iat=iat,
            exp=exp
        )