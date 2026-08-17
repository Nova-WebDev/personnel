from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.unit_entity import UnitEntity


class CreateUnit:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, name: str, branch_id: int) -> UnitEntity:
        return await self.personnel_repo.create_unit(name, branch_id)