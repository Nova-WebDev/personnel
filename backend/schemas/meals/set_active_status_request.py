from pydantic import BaseModel


class SetActiveStatusRequest(BaseModel):
    is_active: bool