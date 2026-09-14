from pydantic import BaseModel


class TimePolicyResponse(BaseModel):
    id: str
    target_weekday: str
    cutoff_hours_before: int