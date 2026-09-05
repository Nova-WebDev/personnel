from pydantic import BaseModel


class TokenResponse(BaseModel):
    refresh_token: str
    access_token_expires_at: int