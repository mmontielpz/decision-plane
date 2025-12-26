# app/api/routes.py

from fastapi import APIRouter

# -------------------------
# System-facing routers
# -------------------------
from app.ingestion.routes import router as ingestion_router

# -------------------------
# Product-facing routers
# -------------------------
from app.api.product.documents import router as product_documents_router

# -------------------------
# Root API router
# -------------------------
router = APIRouter()

# Ingestion / internal system endpoints
router.include_router(ingestion_router)

# Product-facing endpoints (UI, users)
router.include_router(product_documents_router)
