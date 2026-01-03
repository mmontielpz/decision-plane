from fastapi import APIRouter
from app.serving.dashboard_repository import get_dashboard_summary
from app.api.contracts.dashboard_v1 import DashboardSummaryV1

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("/summary", response_model=DashboardSummaryV1)
def dashboard_summary():
    return get_dashboard_summary()
