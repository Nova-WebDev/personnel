import uuid

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.personnel_detail_entity import PersonnelDetailEntity
from personnel.core.errors.personnel_errors import PersonnelNotFoundError


class GetPersonnelDetail:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, personnel_uuid: uuid.UUID) -> PersonnelDetailEntity:
        personnel = await self.personnel_repo.get_personnel_detail(personnel_uuid)

        if personnel is None:
            raise PersonnelNotFoundError()

        return personnel