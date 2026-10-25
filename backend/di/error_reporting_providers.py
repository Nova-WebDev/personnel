from sqlalchemy import select

from app.data.db import AsyncSessionLocal
from app.errors.error_event_reporter import ErrorEventReporter
from app.events.redis_event_publisher import RedisEventPublisher
from app.redis.redis_client import redis_client
from user.core.entities.permission_level import PermissionLevel
from user.infrastructure.data.models.permission import PermissionModel


async def get_admin_user_ids() -> list[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PermissionModel.user_id).where(PermissionModel.level == PermissionLevel.ADMIN)
        )
        return list(result.scalars().all())


error_event_reporter = ErrorEventReporter(
    event_publisher=RedisEventPublisher(redis_client),
    admin_ids_provider=get_admin_user_ids,
)