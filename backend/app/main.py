from fastapi import FastAPI

app = FastAPI(title="CivicPulse API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}