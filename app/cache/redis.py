import redis.asyncio as redis

from app.config import settings


class RedisCache:
    def __init__(self):
        self.client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def set(self, key: str, value: str) -> None:
        await self.client.set(
            key,
            value,
            ex=settings.redis_ttl,
        )

    async def close(self) -> None:
        await self.client.aclose()
