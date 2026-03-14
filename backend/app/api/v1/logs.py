from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import LogLevel, User
from app.schemas.logs import (
    AlertEventOut,
    AlertRuleCreate,
    AlertRuleOut,
    LogIngestRequest,
    LogIngestResponse,
    LogSearchResponse,
)
from app.services.log_service import LogService

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/ingest", response_model=LogIngestResponse)
def ingest_log(
    payload: LogIngestRequest,
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> LogIngestResponse:
    client_key = LogService.authenticate_ingestion_key(db, x_api_key)
    log = LogService.ingest(db, client_key.organization_id, payload.model_dump())
    return LogIngestResponse(accepted=True, log_id=log.id, normalized_level=log.level)


@router.get("/search", response_model=list[LogSearchResponse])
def search_logs(
    hours: int = Query(24, ge=1, le=168),
    service: str | None = None,
    level: LogLevel | None = None,
    keyword: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[LogSearchResponse]:
    logs = LogService.search(db, user.organization_id, hours, service, level, keyword, page, page_size)
    return [LogSearchResponse.model_validate(item) for item in logs]


@router.post("/alerts/rules", response_model=AlertRuleOut)
def create_alert_rule(
    payload: AlertRuleCreate,
    user: User = Depends(require_roles("admin", "developer")),
    db: Session = Depends(get_db),
) -> AlertRuleOut:
    rule = LogService.create_alert_rule(db, user.organization_id, payload.model_dump())
    return AlertRuleOut.model_validate(rule)


@router.get("/alerts/rules", response_model=list[AlertRuleOut])
def list_alert_rules(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AlertRuleOut]:
    rules = LogService.list_alert_rules(db, user.organization_id)
    return [AlertRuleOut.model_validate(item) for item in rules]


@router.get("/alerts/events", response_model=list[AlertEventOut])
def list_alert_events(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AlertEventOut]:
    events = LogService.list_alert_events(db, user.organization_id)
    return [AlertEventOut.model_validate(item) for item in events]


@router.post("/bootstrap-api-key")
def bootstrap_api_key(
    label: str = Query("default"),
    raw_key: str = Query(..., min_length=16),
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    from app.core.security import hash_api_key
    from app.models.entities import IngestionAPIKey

    existing = db.query(IngestionAPIKey).filter(IngestionAPIKey.label == label, IngestionAPIKey.organization_id == user.organization_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Label already exists")

    key = IngestionAPIKey(key_hash=hash_api_key(raw_key), label=label, organization_id=user.organization_id)
    db.add(key)
    db.commit()
    return {"status": "created", "label": label}
