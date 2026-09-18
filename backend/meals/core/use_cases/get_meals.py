import json

from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.interfaces.meal_cache import IMealCache
from meals.core.entities.meal import Meal
from meals.core.errors.meals_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class GetMeals:
    def __init__(self, meal_repository: IMealRepository, meal_cache: IMealCache):
        self.meal_repository = meal_repository
        self.meal_cache = meal_cache

    async def execute(self, permissions: list[dict]) -> list[Meal]:
        self._authorize(permissions)

        cached = await self.meal_cache.get_all()

        if cached:
            return [self._deserialize(raw) for raw in cached.values()]

        meals = await self.meal_repository.get_all()

        for meal in meals:
            await self.meal_cache.set(meal.id, json.dumps(self._serialize(meal)))

        return meals

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_kitchen = any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions)

        if not (is_admin or is_kitchen):
            raise PermissionDeniedError()

    @staticmethod
    def _serialize(meal: Meal) -> dict:
        return {
            "id": meal.id,
            "title": meal.title,
            "description": meal.description,
            "photo_path": meal.photo_path,
            "is_active": meal.is_active,
        }

    @staticmethod
    def _deserialize(raw: str) -> Meal:
        data = json.loads(raw)
        return Meal(**data)