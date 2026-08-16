from dataclasses import dataclass

@dataclass
class AuthSessionEntity:
    public_id: str
    phone_number: str
    role: int