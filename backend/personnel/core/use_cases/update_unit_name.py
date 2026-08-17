from personnel.core.interfaces.personnel_repository import IPersonnelRepository


class UpdateUnitName:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(self, unit_id: int, name: str) -> None:
        await self.personnel_repo.update_unit_name(unit_id, name)