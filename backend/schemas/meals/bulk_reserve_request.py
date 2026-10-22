from pydantic import BaseModel


class BulkReserveItem(BaseModel):
    user_id: str
    reserve: bool


class BulkReserveRequest(BaseModel):
    meal_plan_id: str
    items: list[BulkReserveItem]