from fastapi.testclient import TestClient

from app.api.routes.locations import location_service
from app.main import app
from app.schemas.location import Location, LocationSearchResponse

client = TestClient(app)


async def mock_search(query: str) -> LocationSearchResponse:
    return LocationSearchResponse(
        results=[
            Location(
                name="Bilbao",
                country="Spain",
                country_code="es",
                latitude=43.2630,
                longitude=-2.9350,
            )
        ]
    )


def test_search_locations(monkeypatch):
    monkeypatch.setattr(
        location_service,
        "search",
        mock_search,
    )

    response = client.get(
        "/api/v1/locations/search",
        params={"q": "Bilbao"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 1
    assert data["results"][0]["name"] == "Bilbao"
    assert data["results"][0]["country"] == "Spain"
    assert data["results"][0]["country_code"] == "es"
    assert data["results"][0]["latitude"] == 43.2630
    assert data["results"][0]["longitude"] == -2.9350


def test_search_locations_query_too_short():
    response = client.get(
        "/api/v1/locations/search",
        params={"q": "B"},
    )

    assert response.status_code == 422
