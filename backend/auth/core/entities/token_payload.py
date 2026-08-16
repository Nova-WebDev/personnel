from dataclasses import dataclass

@dataclass
class TokenPayload:
    phone_number: str
    public_id: str
    role: int
    iat: int
    exp: int
