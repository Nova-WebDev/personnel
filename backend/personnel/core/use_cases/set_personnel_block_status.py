import uuid

from personnel.core.interfaces.personnel_repository import IPersonnelRepository


class SetPersonnelBlockStatus:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, personnel_uuid: uuid.UUID, is_blocked: bool) -> None:
        await self.personnel_repo.set_personnel_block_status(personnel_uuid, is_blocked)