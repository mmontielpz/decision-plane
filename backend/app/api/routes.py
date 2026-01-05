from fastapi import APIRouter

# -------------------------
# System-facing routers
# -------------------------
from app.ingestion.routes import router as ingestion_router

# -------------------------
# Product-facing routers
# -------------------------
from app.api.product.documents import router as product_documents_router
from app.api.product.decision_outcomes import router as decision_outcomes_router

# -------------------------
# Replay / inspection routers
# -------------------------
from app.api.replay.routes import router as replay_router

# -------------------------
# Dashboard / summary routers
# -------------------------
from app.api.product.dashboard import router as dashboard_router

# -------------------------
# Admin / operational routers
# -------------------------
from app.api.admin.routes import router as admin_router

# -------------------------
# Root API router
# -------------------------
router = APIRouter(prefix="/api")

# Ingestion / internal system endpoints
router.include_router(ingestion_router)

# Product-facing endpoints (UI, users)
router.include_router(product_documents_router)
router.include_router(decision_outcomes_router)

# Replay / inspection endpoints (read-only)
router.include_router(replay_router)

# Dashboard / product summary endpoints
router.include_router(dashboard_router)

# Admin / operational endpoints (seed, maintenance)
router.include_router(admin_router)
