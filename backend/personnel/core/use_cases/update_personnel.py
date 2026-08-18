import uuid

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition


class UpdatePersonnel:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(
        self,
        personnel_uuid: uuid.UUID,
        personnel_id: str,
        first_name: str,
        last_name: str,
        branch_id: int,
        unit_id: int | None,
        position: PersonnelPosition | None,
    ) -> PersonnelEntity:
        return await self.personnel_repo.update_personnel(
            personnel_uuid=personnel_uuid,
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            position=position,
        )