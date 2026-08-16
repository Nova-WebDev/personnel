import json
from typing import Optional
from redis.asyncio import Redis

from app.utils.logger import logger
from auth.core.interfaces.auth_store import IAuthStore
from auth.core.entities.auth_session_entity import AuthSessionEntity


class AuthStore(IAuthStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 60 * 60 * 24 * 30):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(public_id: str) -> str:
        return f"auth:userdata:{public_id}"

    @staticmethod
    def _serialize(data: AuthSessionEntity) -> str:
        return json.dumps({
            "phone_number": data.phone_number,
            "role": data.role,
        })

    @staticmethod
    def _deserialize(public_id: str, raw: str) -> AuthSessionEntity:
        data = json.loads(raw)

        return AuthSessionEntity(
            public_id=public_id,
            phone_number=data["phone_number"],
            role=data["role"],
        )

    async def get(self, public_id: str) -> Optional[AuthSessionEntity]:
        key = self._key(public_id)

        try:
            raw = await self.redis.get(key)
            if not raw:
                return None

            await self.redis.expire(key, self.ttl)

            return self._deserialize(public_id, raw)

        except Exception as e:
            logger.error(f"AuthStore.get failed: {e}")
            return None

    async def save(self, data: AuthSessionEntity) -> None:
        key = self._key(data.public_id)

        try:
            payload = self._serialize(data)
            await self.redis.set(key, payload, ex=self.ttl)

        except Exception as e:
            logger.error(f"AuthStore.save failed: {e}")
            return None

    async def delete(self, public_id: str) -> None:
        key = self._key(public_id)

        try:
            await self.redis.delete(key)

        except Exception as e:
            logger.error(f"AuthStore.delete failed: {e}")
            return None

    async def change_role(self, public_id: str, role: int) -> None:
        key = self._key(public_id)

        try:
            raw = await self.redis.get(key)
            if not raw:
                return None

            session = self._deserialize(public_id, raw)
            session.role = role

            await self.redis.set(key, self._serialize(session), ex=self.ttl)

        except Exception as e:
            logger.error(f"AuthStore.change_role failed: {e}")
            return None