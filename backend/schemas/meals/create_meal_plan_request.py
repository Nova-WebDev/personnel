from datetime import date

from pydantic import BaseModel


class CreateMealPlanRequest(BaseModel):
    plan_date: date
    meal_id: str