from dataclasses import dataclass


@dataclass
class AccessTokenResult:
    token: str
    expires_at: int