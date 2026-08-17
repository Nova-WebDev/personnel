from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.branch_entity import BranchEntity


class UpdateBranch:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, branch_id: int, name: str) -> BranchEntity:
        return await self.personnel_repo.update_branch(branch_id, name)