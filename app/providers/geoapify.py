import httpx

from app.config import settings


class GeoapifyProvider:
    BASE_URL = "https://api.geoapify.com/v1/geocode/search"

    async def search(self, query: str) -> dict:
        params = {
            "text": query,
            "apiKey": settings.geoapify_api_key,
            "format": "json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
                timeout=10,
            )

        response.raise_for_status()

        return response.json()
