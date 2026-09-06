import pytest

from app.cache.redis import RedisCache


class FakeRedisClient:
    def __init__(self):
        self.data = {}

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value, ex):
        self.data[key] = value

        assert ex == 3600

    async def aclose(self):
        pass


@pytest.mark.asyncio
async def test_redis_set_and_get():
    cache = RedisCache()

    fake_client = FakeRedisClient()
    cache.client = fake_client

    await cache.set("test:key", "test-value")

    result = await cache.get("test:key")

    assert result == "test-value"


@pytest.mark.asyncio
async def test_redis_get_missing_key():
    cache = RedisCache()

    fake_client = FakeRedisClient()
    cache.client = fake_client

    result = await cache.get("does:not:exist")

    assert result is None


@pytest.mark.asyncio
async def test_redis_close():
    cache = RedisCache()

    fake_client = FakeRedisClient()
    cache.client = fake_client

    await cache.close()
