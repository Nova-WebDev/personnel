from datetime import date

from pydantic import BaseModel

from schemas.meals.meal_response import MealResponse


class MealPlanResponse(BaseModel):
    id: str
    plan_date: date
    meal: MealResponse
    is_reserved: bool