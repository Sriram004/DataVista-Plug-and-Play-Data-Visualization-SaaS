from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.security import hash_api_key
from app.models.entities import AlertEvent, AlertRule, IngestionAPIKey, LogEvent, LogLevel
from app.services.log_processing_service import LogProcessingService
from app.services.queue_service import QueueService


class LogService:
    INGEST_LIMIT_PER_MINUTE = 120
    _request_counts: dict[str, tuple[int, datetime]] = {}

    @classmethod
    def authenticate_ingestion_key(cls, db: Session, api_key: str) -> IngestionAPIKey:
        hashed = hash_api_key(api_key)
        key = (
            db.query(IngestionAPIKey)
            .filter(IngestionAPIKey.key_hash == hashed, IngestionAPIKey.is_active.is_(True))
            .first()
        )
        if key is None:
            raise HTTPException(status_code=401, detail="Invalid ingestion API key")
        cls._check_rate_limit(hashed)
        return key

    @classmethod
    def ingest(cls, db: Session, organization_id: int, payload: dict) -> LogEvent:
        QueueService.enqueue(payload)
        raw = QueueService.dequeue() or payload
        normalized = LogProcessingService.normalize(raw)
        log = LogEvent(organization_id=organization_id, **normalized)
        db.add(log)
        db.commit()
        db.refresh(log)
        cls.evaluate_alerts(db, organization_id, log.service)
        return log

    @staticmethod
    def search(
        db: Session,
        organization_id: int,
        hours: int,
        service: str | None,
        level: LogLevel | None,
        keyword: str | None,
        page: int,
        page_size: int,
    ) -> list[LogEvent]:
        since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=hours)
        query = db.query(LogEvent).filter(LogEvent.organization_id == organization_id, LogEvent.timestamp >= since)
        if service:
            query = query.filter(LogEvent.service == service)
        if level:
            query = query.filter(LogEvent.level == level)
        if keyword:
            query = query.filter(LogEvent.message.ilike(f"%{keyword}%"))
        return (
            query.order_by(LogEvent.timestamp.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @staticmethod
    def create_alert_rule(db: Session, organization_id: int, payload: dict) -> AlertRule:
        rule = AlertRule(organization_id=organization_id, **payload)
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    @staticmethod
    def list_alert_rules(db: Session, organization_id: int) -> list[AlertRule]:
        return db.query(AlertRule).filter(AlertRule.organization_id == organization_id).all()

    @staticmethod
    def list_alert_events(db: Session, organization_id: int) -> list[AlertEvent]:
        return (
            db.query(AlertEvent)
            .filter(AlertEvent.organization_id == organization_id)
            .order_by(AlertEvent.triggered_at.desc())
            .limit(100)
            .all()
        )

    @classmethod
    def evaluate_alerts(cls, db: Session, organization_id: int, service_name: str) -> None:
        rules = (
            db.query(AlertRule)
            .filter(AlertRule.organization_id == organization_id, AlertRule.is_active.is_(True))
            .all()
        )
        for rule in rules:
            since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=rule.window_minutes)
            conditions = [
                LogEvent.organization_id == organization_id,
                LogEvent.timestamp >= since,
                LogEvent.level == rule.level,
            ]
            if rule.service != "*":
                conditions.append(LogEvent.service == rule.service)
            count = db.query(LogEvent).filter(and_(*conditions)).count()
            if count >= rule.threshold:
                event = AlertEvent(
                    rule_id=rule.id,
                    organization_id=organization_id,
                    message=f"Rule '{rule.name}' triggered with {count} logs in {rule.window_minutes}m",
                    payload_json={"count": count, "service": service_name, "channel": rule.channel.value},
                )
                db.add(event)
        db.commit()

    @classmethod
    def _check_rate_limit(cls, key_hash: str) -> None:
        now = datetime.now(timezone.utc)
        count, window_start = cls._request_counts.get(key_hash, (0, now))
        if (now - window_start).total_seconds() >= 60:
            cls._request_counts[key_hash] = (1, now)
            return
        if count >= cls.INGEST_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        cls._request_counts[key_hash] = (count + 1, window_start)
