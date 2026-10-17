from datetime import date, datetime, time, timedelta, timezone

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


def resolve_deadline_utc(plan_date: date, cutoff_hours_before: int) -> datetime:
    meal_moment = datetime.combine(plan_date, MEAL_REFERENCE_TIME, tzinfo=timezone.utc)
    return meal_moment - timedelta(hours=cutoff_hours_before)