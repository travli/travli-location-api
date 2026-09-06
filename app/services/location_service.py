import json

from app.cache.redis import RedisCache
from app.providers.geoapify import GeoapifyProvider
from app.schemas.location import Location, LocationSearchResponse


class LocationService:
    def __init__(self):
        self.provider = GeoapifyProvider()
        self.cache = RedisCache()

    async def search(self, query: str) -> LocationSearchResponse:
        cache_key = f"location:search:{query.strip().lower()}"

        cached = await self.cache.get(cache_key)

        if cached:
            return LocationSearchResponse(
                results=[Location(**location) for location in json.loads(cached)]
            )

        data = await self.provider.search(query)

        locations = []

        for result in data.get("results", []):
            locations.append(
                Location(
                    name=(
                        result.get("city")
                        or result.get("name")
                        or result.get("formatted")
                    ),
                    country=result.get("country", ""),
                    country_code=result.get("country_code", ""),
                    latitude=result["lat"],
                    longitude=result["lon"],
                )
            )

        await self.cache.set(
            cache_key,
            json.dumps([location.model_dump() for location in locations]),
        )

        return LocationSearchResponse(results=locations)
