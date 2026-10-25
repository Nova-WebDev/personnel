from pydantic import BaseModel


class SetGuestCountRequest(BaseModel):
    meal_plan_id: str
    unit_id: str
    guest_count: int