from typing import Any

from pydantic import BaseModel, Field


class EventEntity(BaseModel):
    targets: list[str] = Field(min_length=1)
    event: str = Field(min_length=1)
    scope: str
    meta: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)
