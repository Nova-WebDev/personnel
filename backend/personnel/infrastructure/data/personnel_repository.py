from sqlalchemy.ext.asyncio import AsyncSession

from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.branch_entity import BranchEntity
from personnel.infrastructure.data.models import Branch


class PersonnelRepository(IPersonnelRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_branch(self, name: str) -> BranchEntity:
        branch = Branch(name=name)
        self.session.add(branch)
        await self.session.commit()
        await self.session.refresh(branch)

        return BranchEntity(
            id=branch.id,
            name=branch.name
        )
