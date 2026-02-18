from sqlalchemy.orm import Session

from app.models.entities import Dashboard, User
from app.schemas.dashboard import DashboardCreate


class DashboardService:
    @staticmethod
    def create_dashboard(db: Session, user: User, payload: DashboardCreate) -> Dashboard:
        dashboard = Dashboard(
            name=payload.name,
            description=payload.description,
            layout_json=payload.layout_json,
            organization_id=user.organization_id,
            owner_id=user.id,
        )
        db.add(dashboard)
        db.commit()
        db.refresh(dashboard)
        return dashboard

    @staticmethod
    def list_dashboards(db: Session, org_id: int) -> list[Dashboard]:
        return db.query(Dashboard).filter(Dashboard.organization_id == org_id).all()
