from personnel.core.interfaces.personnel_repository import IPersonnelRepository


class DeleteUnit:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, unit_id: int) -> None:
        await self.personnel_repo.delete_unit(unit_id)