from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.interfaces.permission_repository import IPermissionRepository
from user.infrastructure.data.models.permission import PermissionModel
from user.infrastructure.data.models.unit import UnitModel
from user.core.entities.permission_level import PermissionLevel


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_admin_user_ids(self) -> list[str]:
        stmt = select(PermissionModel.user_id).where(
            PermissionModel.level == PermissionLevel.ADMIN
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_global_and_branch_scoped_user_ids(self, branch_id: str) -> list[str]:
        branch_unit_ids = select(UnitModel.id).where(UnitModel.branch_id == branch_id)

        stmt = select(PermissionModel.user_id).where(
            (PermissionModel.group_id.is_(None))
            | (PermissionModel.group_id.in_(branch_unit_ids))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())