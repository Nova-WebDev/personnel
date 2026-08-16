from redis.asyncio import Redis
from auth.core.interfaces.auth_block_store import IBlockStore


class BlockStore(IBlockStore):
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _key(phone_number: str) -> str:
        return f"auth:block:{phone_number}"

    async def is_blocked(self, phone_number: str) -> bool:
        key = self._key(phone_number)
        exists = await self.redis.exists(key)
        return exists == 1

    async def block(self, phone_number: str, seconds: int):
        key = self._key(phone_number)
        await self.redis.set(key, "1", ex=seconds)
