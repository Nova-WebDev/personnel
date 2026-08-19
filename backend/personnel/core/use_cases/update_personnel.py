import uuid

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.interfaces.image_format_validator import IImageFormatValidator
from personnel.core.interfaces.image_processor import IImageProcessor
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition
from personnel.core.errors.personnel_errors import PersonnelNotFoundError


class UpdatePersonnel:
    def __init__(
        self,
        personnel_repo: IPersonnelRepository,
        format_validator: IImageFormatValidator,
        image_processor: IImageProcessor,
    ):
        self.personnel_repo = personnel_repo
        self.format_validator = format_validator
        self.image_processor = image_processor

    async def execute(
        self,
        personnel_uuid: uuid.UUID,
        personnel_id: str,
        first_name: str,
        last_name: str,
        branch_id: int,
        unit_id: int | None,
        position: PersonnelPosition | None,
        file_bytes: bytes | None,
    ) -> PersonnelEntity:
        old_personnel = await self.personnel_repo.get_by_uuid(personnel_uuid)

        if old_personnel is None:
            raise PersonnelNotFoundError()

        photo_path = old_personnel.photo_path

        if file_bytes is not None:
            await self.format_validator.validate(file_bytes)

            if photo_path is not None:
                old_file_id = photo_path.removeprefix("photo/")
                await self.image_processor.delete(old_file_id)

            new_file_id = str(personnel_uuid)
            await self.image_processor.process(
                file_id=new_file_id,
                file_bytes=file_bytes,
                resize_to=(600, 600),
                force_png=True,
            )
            photo_path = f"photo/{new_file_id}"

        personnel = await self.personnel_repo.update_personnel(
            personnel_uuid=personnel_uuid,
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            position=position,
            photo_path=photo_path,
        )

        return personnel