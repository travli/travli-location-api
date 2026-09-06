from fastapi import FastAPI

from app.api.routes.locations import router as locations_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(locations_router)
