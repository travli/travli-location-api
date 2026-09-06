from fastapi import APIRouter, Query

from app.schemas.location import LocationSearchResponse
from app.services.location_service import LocationService

router = APIRouter(prefix="/api/v1/locations", tags=["locations"])

location_service = LocationService()


@router.get("/search", response_model=LocationSearchResponse)
async def search_locations(
    q: str = Query(..., min_length=2),
):
    return await location_service.search(q)
