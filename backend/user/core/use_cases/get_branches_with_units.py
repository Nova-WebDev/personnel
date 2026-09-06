from user.core.interfaces.branch_repository import IBranchRepository
from user.core.entities.branch_with_units import BranchWithUnits


class GetBranchesWithUnits:
    def __init__(self, branch_repository: IBranchRepository):
        self.branch_repository = branch_repository

    async def execute(self, permissions: list[dict]) -> list[BranchWithUnits]:
        has_global_permission = any(p["scope"] is None for p in permissions)

        if has_global_permission:
            return await self.branch_repository.get_all_with_units()

        unit_ids = list({p["scope"] for p in permissions if p["scope"] is not None})

        if not unit_ids:
            return []

        return await self.branch_repository.get_by_unit_ids_with_units(unit_ids)