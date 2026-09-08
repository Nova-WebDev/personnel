from user.core.interfaces.user_repository import IUserRepository
from app.interfaces.image_processor import IImageProcessor
from user.core.interfaces.qr_code_generator import IQRCodeGenerator
from user.core.errors.user_errors import PermissionDeniedError
from user.core.entities.permission_level import PermissionLevel
from app.settings import settings

QR_FOLDER = "qrcode"


class GetUserQrCode:
    def __init__(
        self,
        user_repository: IUserRepository,
        image_processor: IImageProcessor,
        qr_code_generator: IQRCodeGenerator,
    ):
        self.user_repository = user_repository
        self.image_processor = image_processor
        self.qr_code_generator = qr_code_generator

    async def execute(self, user_id: str, permissions: list[dict]) -> bytes:
        user = await self.user_repository.get_by_id(user_id)
        self._authorize(user.unit_id, permissions)

        if await self.image_processor.exists(QR_FOLDER, user_id):
            return await self.image_processor.load(QR_FOLDER, user_id)

        data = f"{settings.frontend_domain}/card/{user_id}"
        qr_bytes = await self.qr_code_generator.generate(data)

        await self.image_processor.save_raw(QR_FOLDER, user_id, qr_bytes)

        return qr_bytes

    @staticmethod
    def _authorize(unit_id: str | None, permissions: list[dict]) -> None:
        is_admin = any(p["level"] == PermissionLevel.ADMIN.value for p in permissions)
        is_hr_for_unit = (
            unit_id is not None
            and any(p["level"] == PermissionLevel.HR_MANAGER.value and p["scope"] == unit_id for p in permissions)
        )

        if not (is_admin or is_hr_for_unit):
            raise PermissionDeniedError()