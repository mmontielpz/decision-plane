from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.models import init_db

app = FastAPI(
    title="Risk-Aware ML System",
    description="Ingestion service (skeleton)",
    version="0.1.0",
)


app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}
