from pydantic import BaseModel


class Location(BaseModel):
    name: str
    country: str
    country_code: str
    latitude: float
    longitude: float


class LocationSearchResponse(BaseModel):
    results: list[Location]
