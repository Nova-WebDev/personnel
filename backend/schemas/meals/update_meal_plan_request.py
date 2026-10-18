from pydantic import BaseModel


class UpdateMealPlanRequest(BaseModel):
    meal_id: str