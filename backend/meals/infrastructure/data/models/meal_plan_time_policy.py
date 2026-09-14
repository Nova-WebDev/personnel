from dataclasses import dataclass

from meals.core.entities.week_day import WeekDay


@dataclass
class MealPlanTimePolicyModel:
    id: str
    target_weekday: WeekDay
    cutoff_hours_before: int