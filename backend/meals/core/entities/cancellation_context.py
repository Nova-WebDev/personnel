from dataclasses import dataclass
from datetime import date


@dataclass
class CancellationContext:
    plan_date: date
    user_unit_id: str | None