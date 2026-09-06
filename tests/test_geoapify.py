import pytest

from app.providers.geoapify import GeoapifyProvider


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
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


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, url, params, timeout):
        assert url == "https://api.geoapify.com/v1/geocode/search"
        assert params["text"] == "Bilbao"
        assert "apiKey" in params
        assert params["format"] == "json"
        assert timeout == 10

        return FakeResponse()


@pytest.mark.asyncio
async def test_geoapify_search(monkeypatch):
    monkeypatch.setattr(
        "app.providers.geoapify.httpx.AsyncClient",
        lambda: FakeAsyncClient(),
    )

    provider = GeoapifyProvider()

    result = await provider.search("Bilbao")

    assert "results" in result
    assert result["results"][0]["city"] == "Bilbao"
