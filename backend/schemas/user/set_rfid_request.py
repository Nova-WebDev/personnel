from pydantic import BaseModel, Field


class SetRfidRequest(BaseModel):
    rfid_card_id: str | None = Field(default=None, pattern=r"^[0-9A-Fa-f]{10}$")