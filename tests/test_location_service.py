import json

import pytest

from app.services.location_service import LocationService


class FakeCache:
    def __init__(self, cached=None):
        self.cached = cached
        self.saved = None

    async def get(self, key):
        return self.cached

    async def set(self, key, value):
        self.saved = {
            "key": key,
            "value": value,
        }


class FakeProvider:
    def __init__(self):
        self.called = False

    async def search(self, query):
        self.called = True

        return {
            "results": [
                {
                    "city": "Bilbao",
                    "country": "Spain",
                    "country_code": "es",
                    "lat": 43.2630,
                    "lon": -2.9350,
                }
            ]
        }


@pytest.mark.asyncio
async def test_search_uses_cache():
    cached_data = json.dumps(
        [
            {
                "name": "Bilbao",
                "country": "Spain",
                "country_code": "es",
                "latitude": 43.2630,
                "longitude": -2.9350,
            }
        ]
    )

    service = LocationService()

    cache = FakeCache(cached=cached_data)
    provider = FakeProvider()

    service.cache = cache
    service.provider = provider

    result = await service.search("Bilbao")

    assert len(result.results) == 1
    assert result.results[0].name == "Bilbao"

    assert provider.called is False


@pytest.mark.asyncio
async def test_search_calls_provider_when_cache_is_empty():
    service = LocationService()

    cache = FakeCache()
    provider = FakeProvider()

    service.cache = cache
    service.provider = provider

    result = await service.search("Bilbao")

    assert len(result.results) == 1
    assert result.results[0].name == "Bilbao"

    assert provider.called is True
    assert cache.saved is not None
    assert cache.saved["key"] == "location:search:bilbao"


@pytest.mark.asyncio
async def test_search_normalizes_provider_response():
    service = LocationService()

    service.cache = FakeCache()
    service.provider = FakeProvider()

    result = await service.search("Bilbao")

    location = result.results[0]

    assert location.name == "Bilbao"
    assert location.country == "Spain"
    assert location.country_code == "es"
    assert location.latitude == 43.2630
    assert location.longitude == -2.9350
