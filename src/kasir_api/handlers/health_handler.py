from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from kasir_api.models.health import HealthResponse
from kasir_api.repositories.db import pool
from kasir_api.repositories.health_repository import HealthRepository
from kasir_api.services.health_service import HealthService

router = APIRouter(tags=["health"])


def get_service() -> HealthService  :
    repository = HealthRepository(pool)
    return HealthService(repository)


@router.get("/health", response_model=HealthResponse)
async def health_check(service: HealthService = Depends(get_service)):
    response = await service.get_health()

    if response.status != "healthy":
        return JSONResponse(content=response.model_dump(), status_code=503)

    return response
