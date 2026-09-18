from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.interfaces.meal_cache import IMealCache
from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel


class SetMealActiveStatus:
    def __init__(
        self,
        meal_repository: IMealRepository,
        event_publisher: IEventPublisher,
        meal_cache: IMealCache,
    ):
        self.meal_repository = meal_repository
        self.event_publisher = event_publisher
        self.meal_cache = meal_cache

    async def execute(self, meal_id: str, is_active: bool, permissions: list[dict]) -> None:
        self._authorize(permissions)

        meal = await self.meal_repository.set_active_status(meal_id, is_active)

        await self.meal_cache.clear()

        await self.event_publisher.publish(
            event="meal.active_status_changed",
            scope="meal",
            data={"id": meal.id, "is_active": meal.is_active},
            targets=["*"],
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_kitchen = any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions)

        if not (is_admin or is_kitchen):
            raise PermissionDeniedError()