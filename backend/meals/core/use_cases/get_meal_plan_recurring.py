from meals.core.entities.meal_plan_recurring import MealPlanRecurring
from meals.core.errors.meals_errors import PermissionDeniedError
from meals.core.interfaces.meal_plan_recurring_repository import IMealPlanRecurringRepository
from user.core.entities.permission_level import PermissionLevel


class GetMealPlanRecurring:
    def __init__(self, recurring_repository: IMealPlanRecurringRepository):
        self.recurring_repository = recurring_repository

    async def execute(self, permissions: list[dict]) -> list[MealPlanRecurring]:
        self._authorize(permissions)
        return await self.recurring_repository.get_all()

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        if not any(p["level"] == PermissionLevel.ADMIN.value for p in permissions):
            raise PermissionDeniedError()