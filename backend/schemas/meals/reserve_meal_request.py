from pydantic import BaseModel


class ReserveMealRequest(BaseModel):
    meal_plan_id: str