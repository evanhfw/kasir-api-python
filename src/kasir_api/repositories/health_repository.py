import time

from psycopg_pool import AsyncConnectionPool

from kasir_api.models.health import CheckResult


class HealthRepository:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def ping_database(self) -> CheckResult:
        try:
            start = time.perf_counter()
            async with self.pool.connection() as conn:
                await conn.execute("SELECT 1")
            latency = (time.perf_counter() - start) * 1000
            return CheckResult(status="healthy", latency_ms=round(latency, 2))
        except Exception as e:
            return CheckResult(status="unhealthy", error=str(e))
