from abc import ABC, abstractmethod
from datetime import date

from meals.core.entities.inviter_guest_row import InviterGuestRow


class IGuestRepository(ABC):
    @abstractmethod
    async def get_plan_context(self, meal_plan_id: str) -> tuple[date, bool]:
        pass

    @abstractmethod
    async def set_guest_count(
        self, meal_plan_id: str, unit_id: str, invited_by: str, plan_date: date, guest_count: int
    ) -> int:
        pass

    @abstractmethod
    async def get_inviter_guests(self, user_id: str, day: date) -> list[InviterGuestRow]:
        pass

    @abstractmethod
    async def mark_inviter_guests_used(self, user_id: str, day: date) -> dict[str, int]:
        pass