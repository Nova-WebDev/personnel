from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.interfaces.meal_cache import IMealCache
from app.interfaces.image_format_validator import IImageFormatValidator
from app.interfaces.image_processor import IImageProcessor
from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel

MEAL_PHOTO_FOLDER = "meal"
MEAL_PHOTO_SIZE = (1200, 1200)


class UpdateMeal:
    def __init__(
        self,
        meal_repository: IMealRepository,
        event_publisher: IEventPublisher,
        meal_cache: IMealCache,
        format_validator: IImageFormatValidator,
        image_processor: IImageProcessor,
    ):
        self.meal_repository = meal_repository
        self.event_publisher = event_publisher
        self.meal_cache = meal_cache
        self.format_validator = format_validator
        self.image_processor = image_processor

    async def execute(
        self,
        meal_id: str,
        title: str,
        permissions: list[dict],
        description: str | None = None,
        file_bytes: bytes | None = None,
    ) -> None:
        self._authorize(permissions)

        if file_bytes is not None:
            await self.format_validator.validate(file_bytes)

        current = await self.meal_repository.get_by_id(meal_id)

        meal = await self.meal_repository.update(
            meal_id=meal_id,
            title=title,
            description=description,
        )

        if file_bytes is not None:
            await self.image_processor.process(
                folder=MEAL_PHOTO_FOLDER,
                file_id=meal_id,
                file_bytes=file_bytes,
                resize_to=MEAL_PHOTO_SIZE,
                force_png=True,
            )

            if current.photo_path is None:
                photo_path = f"{MEAL_PHOTO_FOLDER}/{meal_id}"
                await self.meal_repository.set_photo_path(meal_id, photo_path)
                meal.photo_path = photo_path

        await self.meal_cache.clear()

        await self.event_publisher.publish(
            event="meal.updated",
            scope="meal",
            data={
                "id": meal.id,
                "title": meal.title,
                "description": meal.description,
                "photo_path": meal.photo_path,
                "is_active": meal.is_active,
            },
            targets=["*"],
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_kitchen = any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions)

        if not (is_admin or is_kitchen):
            raise PermissionDeniedError()