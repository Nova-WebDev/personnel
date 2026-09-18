from pydantic import BaseModel


class MealResponse(BaseModel):
    id: str
    title: str
    description: str | None
    photo_path: str | None
    is_active: bool