from datetime import date

from pydantic import BaseModel


class RecurringItemResponse(BaseModel):
    target_date: date
    meal_id: str | None