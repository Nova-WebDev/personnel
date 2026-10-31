from pydantic import BaseModel, Field


class TimePolicyInput(BaseModel):
    target_weekday: str
    cutoff_before: str = Field(pattern=r"^\d{1,3}:[0-5]\d$")


class SetTimePoliciesRequest(BaseModel):
    policies: list[TimePolicyInput]