
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.cache.redis_client import check_rate_limit
from app.routes.complaints import router as complaints_router
from app.routes.statistics import router as statistics_router

app = FastAPI(title="CivicPulse API")


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if os.getenv("CIVICPULSE_TESTING") == "1":
        return await call_next(request)

    client_id = request.client.host if request.client else "unknown"
    allowed, retry_after = check_rate_limit(client_id)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(retry_after)},
        )

    return await call_next(request)


app.include_router(complaints_router)
app.include_router(statistics_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}
