from dataclasses import dataclass, field


@dataclass
class TokenPayload:
    id: str
    phone_number: str
    iat: int
    exp: int
    permissions: list[dict] = field(default_factory=list)