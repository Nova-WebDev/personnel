from datetime import date

from pydantic import BaseModel


class RecurringItem(BaseModel):
    target_date: date
    meal_id: str | None = None


class SetRecurringRequest(BaseModel):
    items: list[RecurringItem]