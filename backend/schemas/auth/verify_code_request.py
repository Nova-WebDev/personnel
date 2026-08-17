from pydantic import BaseModel

class VerifyCodeRequest(BaseModel):
    phone_number: str
    code: str
