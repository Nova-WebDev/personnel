from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.branch_with_units_entity import BranchWithUnitsEntity


class GetAllBranchesWithUnits:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self) -> list[BranchWithUnitsEntity]:
        return await self.personnel_repo.get_all_branches_with_units()