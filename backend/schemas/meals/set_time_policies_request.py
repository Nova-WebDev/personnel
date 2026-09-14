from pydantic import BaseModel


class TimePolicyInput(BaseModel):
    target_weekday: str
    cutoff_hours_before: int


class SetTimePoliciesRequest(BaseModel):
    policies: list[TimePolicyInput]