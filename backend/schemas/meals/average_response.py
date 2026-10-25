from pydantic import BaseModel


class AverageResponse(BaseModel):
    average: float