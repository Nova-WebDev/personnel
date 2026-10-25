from abc import ABC, abstractmethod
from datetime import date


class IReportRepository(ABC):
    @abstractmethod
    async def count_active_users(self) -> int:
        pass

    @abstractmethod
    async def count_active_meals(self) -> int:
        pass

    @abstractmethod
    async def count_branches(self) -> int:
        pass

    @abstractmethod
    async def get_guest_totals(self, date_from: date, date_to: date) -> tuple[int, int]:
        pass

    @abstractmethod
    async def get_daily_meal_counts(self, date_from: date, date_to: date) -> dict[date, int]:
        pass

    @abstractmethod
    async def get_branch_usage(self, date_from: date, date_to: date) -> list[dict]:
        pass