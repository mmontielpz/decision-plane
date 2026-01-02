from fastapi import APIRouter
from app.serving.dashboard_repository import get_dashboard_summary

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("/summary")
def dashboard_summary():
    return get_dashboard_summary()
