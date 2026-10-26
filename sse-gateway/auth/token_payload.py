from dataclasses import dataclass

@dataclass
class TokenPayload:
    public_id: str
    exp: int