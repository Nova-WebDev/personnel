from typing import Optional
from redis.asyncio import Redis
import json

from auth.core.interfaces.auth_code_store import ICodeStore


class CodeStore(ICodeStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 120):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(phone_number: str) -> str:
        return f"auth:session:{phone_number}"

    async def get(self, phone_number: str) -> Optional[dict]:
        key = self._key(phone_number)

        data = await self.redis.get(key)
        if data is None:
            return None

        return json.loads(data)

    async def save(self, phone_number: str, data: dict):
        key = self._key(phone_number)

        await self.redis.set(
            key,
            json.dumps(data),
            ex=self.ttl
        )

    async def delete(self, phone_number: str):
        key = self._key(phone_number)
        await self.redis.delete(key)