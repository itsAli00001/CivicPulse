from fastapi import FastAPI

from app.routes.complaints import router as complaints_router


app = FastAPI(title="CivicPulse API")


app.include_router(complaints_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}