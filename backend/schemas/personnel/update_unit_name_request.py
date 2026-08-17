from pydantic import BaseModel


class UpdateUnitNameRequest(BaseModel):
    name: str