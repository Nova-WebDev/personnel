from pydantic import BaseModel
from typing import Any, List, Dict


class EventEntity(BaseModel):
    targets: List[str]
    event: str
    scope: str
    meta: Dict[str, Any]
    data: Dict[str, Any]