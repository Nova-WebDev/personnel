from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.interfaces.image_format_validator import IImageFormatValidator
from personnel.core.interfaces.image_processor import IImageProcessor
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition


class CreatePersonnel:
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
        personnel_id: str,
        first_name: str,
        last_name: str,
        branch_id: int,
        unit_id: int | None = None,
        file_bytes: bytes | None = None,
        position: PersonnelPosition | None = None,
    ) -> PersonnelEntity:
        photo_path = None

        if file_bytes is not None:
            await self.format_validator.validate(file_bytes)

        personnel = await self.personnel_repo.create_personnel(
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            photo_path=photo_path,
            position=position,
        )

        if file_bytes is not None:
            file_id = str(personnel.uuid)
            await self.image_processor.process(
                file_id=file_id,
                file_bytes=file_bytes,
                resize_to=(600, 600),
                force_png=True,
            )
            photo_path = f"photo/{file_id}"
            await self.personnel_repo.update_photo_path(personnel.uuid, photo_path)

        return PersonnelEntity(
            uuid=personnel.uuid,
            personnel_id=personnel.personnel_id,
            first_name=personnel.first_name,
            last_name=personnel.last_name,
            branch_id=personnel.branch_id,
            unit_id=personnel.unit_id,
            photo_path=photo_path,
            position=personnel.position,
            is_blocked=personnel.is_blocked,
        )