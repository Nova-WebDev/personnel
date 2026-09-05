import json
from typing import Optional
from redis.asyncio import Redis

from auth.core.interfaces.auth_store import IAuthStore
from auth.core.entities.auth_session_entity import AuthSessionEntity


class AuthStore(IAuthStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 60 * 60 * 24 * 30):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(user_id: str) -> str:
        return f"auth:userdata:{user_id}"

    @staticmethod
    def _serialize(data: AuthSessionEntity) -> str:
        return json.dumps({
            "phone_number": data.phone_number,
            "is_blocked": data.is_blocked,
            "permissions": data.permissions,
        })

    @staticmethod
    def _deserialize(user_id: str, raw: str) -> AuthSessionEntity:
        data = json.loads(raw)

        return AuthSessionEntity(
            id=user_id,
            phone_number=data["phone_number"],
            is_blocked=data["is_blocked"],
            permissions=data["permissions"],
        )

    async def get(self, user_id: str) -> Optional[AuthSessionEntity]:
        key = self._key(user_id)
        raw = await self.redis.get(key)

        if not raw:
            return None

        await self.redis.expire(key, self.ttl)
        return self._deserialize(user_id, raw)

    async def save(self, data: AuthSessionEntity) -> None:
        key = self._key(data.id)
        payload = self._serialize(data)
        await self.redis.set(key, payload, ex=self.ttl)

    async def delete(self, user_id: str) -> None:
        await self.redis.delete(self._key(user_id))

    async def update_permissions(self, user_id: str, permissions: list[dict]) -> None:
        key = self._key(user_id)
        raw = await self.redis.get(key)

        if not raw:
            return

        session = self._deserialize(user_id, raw)
        session.permissions = permissions

        await self.redis.set(key, self._serialize(session), ex=self.ttl)
