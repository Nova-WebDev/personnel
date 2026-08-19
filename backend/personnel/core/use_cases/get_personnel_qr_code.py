import uuid

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.interfaces.qr_code_generator import IQRCodeGenerator
from personnel.core.interfaces.qr_rate_limiter import IQRRateLimiter
from personnel.core.errors.personnel_errors import PersonnelNotFoundError, QRCodeRateLimitedError


class GetPersonnelQRCode:
    def __init__(
        self,
        personnel_repo: IPersonnelRepository,
        qr_generator: IQRCodeGenerator,
        rate_limiter: IQRRateLimiter,
        domain: str,
    ):
        self.personnel_repo = personnel_repo
        self.qr_generator = qr_generator
        self.rate_limiter = rate_limiter
        self.domain = domain

    async def execute(self, personnel_uuid: uuid.UUID) -> bytes:
        personnel = await self.personnel_repo.get_by_uuid(personnel_uuid)

        if personnel is None:
            raise PersonnelNotFoundError()

        allowed = await self.rate_limiter.is_allowed(personnel_uuid)

        if not allowed:
            raise QRCodeRateLimitedError()

        url = f"{self.domain}/{personnel_uuid}"
        return await self.qr_generator.generate(url)