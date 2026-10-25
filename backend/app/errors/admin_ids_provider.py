from sqlalchemy import select

from app.data.db import AsyncSessionLocal
from user.core.entities.permission_level import PermissionLevel
from user.infrastructure.data.models.permission import PermissionModel


async def get_admin_user_ids() -> list[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PermissionModel.user_id).where(PermissionModel.level == PermissionLevel.ADMIN)
        )
        return list(result.scalars().all())