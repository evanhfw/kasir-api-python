import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from kasir_api.repositories.db import pool

router = APIRouter(tags=["health"])


class CheckResult(BaseModel):
    status: str
    latency_ms: float | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    checks: dict[str, CheckResult]


async def check_database() -> CheckResult:
    try:
        start = time.perf_counter()
        async with pool.connection() as conn:
            await conn.execute("SELECT 1")
        latency = (time.perf_counter() - start) * 1000
        return CheckResult(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        return CheckResult(status="unhealthy", error=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_check = await check_database()

    checks = {"database": db_check}

    all_healthy = all(c.status == "healthy" for c in checks.values())
    overall_status = "healthy" if all_healthy else "unhealthy"

    response = HealthResponse(status=overall_status, checks=checks)

    if not all_healthy:
        return JSONResponse(content=response.model_dump(), status_code=503)

    return response
