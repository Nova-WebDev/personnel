import uuid

from meals.core.interfaces.meal_repository import IMealRepository
from meals.core.interfaces.meal_cache import IMealCache
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.image_format_validator import IImageFormatValidator
from app.interfaces.image_processor import IImageProcessor
from app.interfaces.event_publisher import IEventPublisher
from meals.core.errors.meals_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel

MEAL_PHOTO_FOLDER = "meal"
MEAL_PHOTO_SIZE = (1200, 1200)


class CreateMeal:
    def __init__(
        self,
        meal_repository: IMealRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
        format_validator: IImageFormatValidator,
        image_processor: IImageProcessor,
        meal_cache: IMealCache,
    ):
        self.meal_repository = meal_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher
        self.format_validator = format_validator
        self.image_processor = image_processor
        self.meal_cache = meal_cache

    async def execute(
        self,
        title: str,
        permissions: list[dict],
        description: str | None = None,
        file_bytes: bytes | None = None,
    ) -> None:
        self._authorize(permissions)

        if file_bytes is not None:
            await self.format_validator.validate(file_bytes)

        meal_id = str(uuid.uuid4())
        photo_path = f"{MEAL_PHOTO_FOLDER}/{meal_id}" if file_bytes is not None else None

        meal = await self.meal_repository.create(
            meal_id=meal_id,
            title=title,
            description=description,
            photo_path=photo_path,
        )

        if file_bytes is not None:
            await self.image_processor.process(
                folder=MEAL_PHOTO_FOLDER,
                file_id=meal_id,
                file_bytes=file_bytes,
                resize_to=MEAL_PHOTO_SIZE,
                force_png=True,
            )

        await self.meal_cache.clear()

        targets = await self.permission_repository.get_admin_and_kitchen_user_ids()

        await self.event_publisher.publish(
            event="meal.created",
            scope="meal",
            data={
                "id": meal.id,
                "title": meal.title,
                "description": meal.description,
                "photo_path": meal.photo_path,
                "is_active": meal.is_active,
            },
            targets=targets,
        )

    @staticmethod
    def _authorize(permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_kitchen = any(p["level"] == PermissionLevel.KITCHEN.value for p in permissions)

        if not (is_admin or is_kitchen):
            raise PermissionDeniedError()