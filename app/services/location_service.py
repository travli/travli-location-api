from app.providers.geoapify import GeoapifyProvider
from app.schemas.location import Location, LocationSearchResponse


class LocationService:
    def __init__(self):
        self.provider = GeoapifyProvider()

    async def search(self, query: str) -> LocationSearchResponse:
        data = await self.provider.search(query)

        locations = []

        for result in data.get("results", []):
            locations.append(
                Location(
                    name=result.get("city")
                    or result.get("name")
                    or result.get("formatted"),
                    country=result.get("country", ""),
                    country_code=result.get("country_code", ""),
                    latitude=result["lat"],
                    longitude=result["lon"],
                )
            )

        return LocationSearchResponse(results=locations)
