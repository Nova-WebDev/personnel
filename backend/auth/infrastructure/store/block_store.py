from redis.asyncio import Redis
from auth.core.interfaces.auth_block_store import IBlockStore


class BlockStore(IBlockStore):
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _key(phone_number: str) -> str:
        return f"auth:block:{phone_number}"

    async def try_block(self, phone_number: str, seconds: int) -> bool:
        key = self._key(phone_number)
        acquired = await self.redis.set(key, "1", ex=seconds, nx=True)
        return acquired is True

    async def force_block(self, phone_number: str, seconds: int) -> None:
        key = self._key(phone_number)
        await self.redis.set(key, "1", ex=seconds)