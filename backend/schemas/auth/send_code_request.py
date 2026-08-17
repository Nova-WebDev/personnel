from pydantic import BaseModel

class SendCodeRequest(BaseModel):
    phone_number: str
