from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.personnel_entity import PersonnelEntity
from personnel.core.entities.position import PersonnelPosition


class CreatePersonnel:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(
        self,
        personnel_id: str,
        first_name: str,
        last_name: str,
        branch_id: int,
        unit_id: int | None = None,
        photo_path: str | None = None,
        position: PersonnelPosition | None = None,
    ) -> PersonnelEntity:
        return await self.personnel_repo.create_personnel(
            personnel_id=personnel_id,
            first_name=first_name,
            last_name=last_name,
            branch_id=branch_id,
            unit_id=unit_id,
            photo_path=photo_path,
            position=position,
        )