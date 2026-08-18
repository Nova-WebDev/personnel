from pydantic import BaseModel


class SetBlockStatusRequest(BaseModel):
    is_blocked: bool