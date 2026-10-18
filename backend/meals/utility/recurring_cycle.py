from dataclasses import dataclass
from datetime import date, timedelta


APPLY_WINDOW_DAYS = 14


@dataclass
class AdvanceResult:
    visited: list[tuple[date, str | None]]
    rotated: list[dict]


def is_contiguous(sorted_dates: list[date]) -> bool:
    return all((b - a).days == 1 for a, b in zip(sorted_dates, sorted_dates[1:]))


def advance(items: list[dict], today: date) -> AdvanceResult:
    queue = [(i["target_date"], i["meal_id"]) for i in items]
    window_end = today + timedelta(days=APPLY_WINDOW_DAYS)

    visited: list[tuple[date, str | None]] = []
    while queue and queue[0][0] < window_end:
        cursor, meal_id = queue.pop(0)
        visited.append((cursor, meal_id))
        last_date = queue[-1][0] if queue else cursor
        queue.append((last_date + timedelta(days=1), meal_id))

    return AdvanceResult(
        visited=visited,
        rotated=[{"target_date": d, "meal_id": m} for d, m in queue],
    )