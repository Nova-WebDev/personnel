from personnel.core.interfaces.image_processor import IImageProcessor


class GetPersonnelPhoto:
    def __init__(self, image_processor: IImageProcessor):
        self.image_processor = image_processor

    async def execute(self, file_id: str) -> bytes:
        return await self.image_processor.load(file_id)