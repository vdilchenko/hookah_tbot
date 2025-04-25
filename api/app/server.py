import uvicorn
from fastapi import FastAPI, status

from core.database import get_top_brands, get_top_flavors
from core.schemas import BrandResponse, FlavorResponse
from config import Config

from pydantic import BaseModel

app = FastAPI(title="Tobacco API")


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"



@app.get("/health", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health():
    return HealthCheck(status="OK")


@app.get("/brands/{flavor}", response_model=list[BrandResponse])
async def brands_by_flavor(flavor: str, limit: int = 10):
    return get_top_brands(flavor, limit)


@app.get("/flavors/{brand}", response_model=list[FlavorResponse])
async def flavors_by_brand(brand: str, limit: int = 10):
    return get_top_flavors(brand, limit)


def run_api():
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT
    )