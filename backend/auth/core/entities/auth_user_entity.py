from dataclasses import dataclass

@dataclass
class AuthUserEntity:
    phone_number: str
    public_id: str
    role: int
    is_blocked: bool