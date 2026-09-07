import uuid

from user.core.interfaces.user_repository import IUserRepository
from user.core.interfaces.permission_repository import IPermissionRepository
from app.interfaces.image_format_validator import IImageFormatValidator
from app.interfaces.image_processor import IImageProcessor
from app.interfaces.event_publisher import IEventPublisher
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel

PHOTO_FOLDER = "profile"


class CreateUser:
    def __init__(
        self,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
        event_publisher: IEventPublisher,
        format_validator: IImageFormatValidator,
        image_processor: IImageProcessor,
    ):
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.event_publisher = event_publisher
        self.format_validator = format_validator
        self.image_processor = image_processor

    async def execute(
        self,
        phone: str,
        first_name: str,
        last_name: str,
        unit_id: str,
        permissions: list[dict],
        personnel_code: str | None = None,
        file_bytes: bytes | None = None,
    ) -> None:
        self._authorize(unit_id, permissions)

        if file_bytes is not None:
            await self.format_validator.validate(file_bytes)

        user_id = str(uuid.uuid4())
        photo_path = f"{PHOTO_FOLDER}/{user_id}" if file_bytes is not None else None

        user = await self.user_repository.create(
            user_id=user_id,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            unit_id=unit_id,
            personnel_code=personnel_code,
            photo_path=photo_path,
        )

        if file_bytes is not None:
            await self.image_processor.process(
                folder=PHOTO_FOLDER,
                file_id=user_id,
                file_bytes=file_bytes,
                resize_to=(600, 600),
                force_png=True,
            )

        targets = await self.permission_repository.get_global_and_unit_scoped_user_ids(unit_id)

        await self.event_publisher.publish(
            event="user.created",
            scope="user",
            data={
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "personnel_code": user.personnel_code,
                "rfid_card_id": user.rfid_card_id,
                "photo_path": user.photo_path,
                "is_blocked": user.is_blocked,
                "created_at": user.created_at.isoformat(),
                "unit_id": user.unit_id,
                "unit_name": user.unit_name,
                "branch_id": user.branch_id,
                "branch_name": user.branch_name,
            },
            targets=targets,
        )

    @staticmethod
    def _authorize(unit_id: str, permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_hr_for_unit = any(
            p["level"] == PermissionLevel.HR_MANAGER.value and p["scope"] == unit_id
            for p in permissions
        )

        if not (is_admin or is_hr_for_unit):
            raise PermissionDeniedError()