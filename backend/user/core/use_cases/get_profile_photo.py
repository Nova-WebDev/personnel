from app.interfaces.image_processor import IImageProcessor
from user.core.errors.user_errors import PhotoNotFoundError

PHOTO_FOLDER = "profile"


class GetProfilePhoto:
    def __init__(self, image_processor: IImageProcessor):
        self.image_processor = image_processor

    async def execute(self, file_id: str) -> bytes:
        try:
            return await self.image_processor.load(PHOTO_FOLDER, file_id)
        except FileNotFoundError:
            raise PhotoNotFoundError()