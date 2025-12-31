import os
from fastapi import APIRouter, HTTPException, status

from app.admin.seed_v1 import run_seed_v1

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed/v1")
def seed_v1():
    enabled = os.getenv("ENABLE_SEED_V1", "false").lower() == "true"
    if not enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seed V1 is disabled",
        )

    summary = run_seed_v1()
    return {
        "status": "ok",
        "seed": "v1",
        "summary": summary,
    }
