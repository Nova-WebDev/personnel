from abc import ABC, abstractmethod
from datetime import date

from meals.core.entities.reservation_context import ReservationContext
from meals.core.entities.voucher_summary import VoucherSummary
from meals.core.entities.cancellation_context import CancellationContext


class IVoucherRepository(ABC):
    @abstractmethod
    async def get_reservation_context(self, user_id: str, meal_plan_id: str) -> ReservationContext:
        pass

    @abstractmethod
    async def upsert_reservation(
        self, user_id: str, meal_plan_id: str, reservation_date: date
    ) -> VoucherSummary | None:
        pass


    @abstractmethod
    async def get_cancellation_context(self, user_id: str, meal_plan_id: str) -> CancellationContext:
        pass

    @abstractmethod
    async def delete_unused(self, user_id: str, meal_plan_id: str) -> bool:
        pass

    @abstractmethod
    async def is_used(self, user_id: str, meal_plan_id: str) -> bool | None:
        pass