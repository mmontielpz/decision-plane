from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.db.models import init_db
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.INIT_DB_ON_STARTUP:
        init_db()
    yield
    # Shutdown (nothing for now)


app = FastAPI(
    title="Risk-Aware ML System",
    description="Ingestion service (skeleton)",
    version="0.1.0",
    lifespan=lifespan,
)

# -------------------------
# CORS (frontend access)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
