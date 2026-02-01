from kasir_api.models.health import HealthResponse
from kasir_api.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(self, repository: HealthRepository):
        self.repository = repository

    async def get_health(self) -> HealthResponse:
        db_check = await self.repository.ping_database()

        checks = {"database": db_check}

        all_healthy = all(c.status == "healthy" for c in checks.values())
        overall_status = "healthy" if all_healthy else "unhealthy"

        return HealthResponse(status=overall_status, checks=checks)
