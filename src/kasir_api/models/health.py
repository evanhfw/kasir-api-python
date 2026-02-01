from pydantic import BaseModel


class CheckResult(BaseModel):
    status: str
    latency_ms: float | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    checks: dict[str, CheckResult]
