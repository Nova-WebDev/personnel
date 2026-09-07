from pydantic import BaseModel


class SetBlockedStatusRequest(BaseModel):
    is_blocked: bool