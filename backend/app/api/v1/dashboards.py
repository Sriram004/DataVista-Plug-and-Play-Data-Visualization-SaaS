from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import User
from app.schemas.dashboard import DashboardCreate, DashboardOut
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.post("", response_model=DashboardOut)
def create_dashboard(
    payload: DashboardCreate,
    user: User = Depends(require_roles("admin", "analyst")),
    db: Session = Depends(get_db),
) -> DashboardOut:
    dashboard = DashboardService.create_dashboard(db, user, payload)
    return DashboardOut.model_validate(dashboard)


@router.get("", response_model=list[DashboardOut])
def list_dashboards(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[DashboardOut]:
    dashboards = DashboardService.list_dashboards(db, user.organization_id)
    return [DashboardOut.model_validate(item) for item in dashboards]
