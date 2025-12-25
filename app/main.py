from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.db.models import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (nothing for now)


app = FastAPI(
    title="Risk-Aware ML System",
    description="Ingestion service (skeleton)",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
