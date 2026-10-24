from pydantic import BaseModel, Field


class RedeemMealRequest(BaseModel):
    rfid_card_id: str = Field(min_length=10, max_length=10, pattern=r"^[0-9A-Fa-f]{10}$")