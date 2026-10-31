from datetime import date, datetime, time, timedelta, timezone

from meals.core.entities.meal_plan_time_policy import MealPlanTimePolicy
from meals.core.entities.week_day import WeekDay

MEAL_REFERENCE_TIME = time(0, 0)

_WEEKDAY_BY_PYTHON_INDEX = {
    0: WeekDay.MONDAY,
    1: WeekDay.TUESDAY,
    2: WeekDay.WEDNESDAY,
    3: WeekDay.THURSDAY,
    4: WeekDay.FRIDAY,
    5: WeekDay.SATURDAY,
    6: WeekDay.SUNDAY,
}


def weekday_of(plan_date: date) -> WeekDay:
    return _WEEKDAY_BY_PYTHON_INDEX[plan_date.weekday()]

def parse_cutoff(cutoff_before: str) -> timedelta:
    hours, minutes = cutoff_before.split(":")
    return timedelta(hours=int(hours), minutes=int(minutes))


def resolve_deadline_utc(plan_date: date, cutoff_before: str) -> datetime:
    meal_moment = datetime.combine(plan_date, MEAL_REFERENCE_TIME, tzinfo=timezone.utc)
    return meal_moment - parse_cutoff(cutoff_before)


def is_deadline_passed(plan_date: date, policies: list[MealPlanTimePolicy], now_utc: datetime) -> bool:
    weekday = weekday_of(plan_date)
    policy = next((p for p in policies if p.target_weekday == weekday), None)
    cutoff_before = policy.cutoff_before if policy is not None else "0:00"

    return now_utc >= resolve_deadline_utc(plan_date, cutoff_before)