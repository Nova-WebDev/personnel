from pydantic import BaseModel


class UpdateUnitRequest(BaseModel):
    name: str