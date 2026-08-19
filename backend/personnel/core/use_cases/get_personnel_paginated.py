from personnel.core.interfaces.personnel_repository import IPersonnelRepository
from personnel.core.entities.personnel_order_by import PersonnelOrderBy


class GetPersonnelPaginated:
    def __init__(self, personnel_repo: IPersonnelRepository):
        self.personnel_repo = personnel_repo

    async def execute(
        self,
        page: int,
        limit: int,
        search: str | None,
        order_by: PersonnelOrderBy = PersonnelOrderBy.CREATED_AT,
        descending: bool = True,
    ) -> dict:
        if page < 1 or limit < 1:
            return {"personnel": [], "total_count": 0}

        offset = (page - 1) * limit

        total_count = await self.personnel_repo.count_personnel(search=search)

        personnel = await self.personnel_repo.get_personnel_paginated(
            offset=offset,
            limit=limit,
            search=search,
            order_by=order_by,
            descending=descending,
        )

        return {
            "personnel": personnel,
            "total_count": total_count,
        }