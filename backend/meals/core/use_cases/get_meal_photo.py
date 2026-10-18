import uuid

from app.interfaces.image_processor import IImageProcessor
from meals.core.errors.meals_errors import MealPhotoNotFoundError

MEAL_PHOTO_FOLDER = "meal"


class GetMealPhoto:
    def __init__(self, image_processor: IImageProcessor):
        self.image_processor = image_processor

    async def execute(self, meal_id: str) -> bytes:
        if not self._is_valid_id(meal_id):
            raise MealPhotoNotFoundError()

        if not await self.image_processor.exists(MEAL_PHOTO_FOLDER, meal_id):
            raise MealPhotoNotFoundError()

        return await self.image_processor.load(MEAL_PHOTO_FOLDER, meal_id)

    @staticmethod
    def _is_valid_id(meal_id: str) -> bool:
        try:
            uuid.UUID(meal_id)
        except ValueError:
            return False
        return True