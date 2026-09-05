from dataclasses import dataclass, field


@dataclass
class AuthUserEntity:
    id: str
    phone_number: str
    is_blocked: bool
    permissions: list[dict] = field(default_factory=list)