from dataclasses import dataclass
from datetime import time

@dataclass
class MealPlanTimePolicy:
    id: str
    day_index: int
    offset_days: int
    cutoff_time: time