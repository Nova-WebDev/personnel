from datetime import date

from pydantic import BaseModel


class MealTrendItem(BaseModel):
    date: date
    count: int