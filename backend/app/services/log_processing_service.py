from datetime import datetime, timezone

from app.models.entities import LogLevel


class LogProcessingService:
    @staticmethod
    def normalize(payload: dict) -> dict:
        ts = payload.get("timestamp")
        if isinstance(ts, str):
            timestamp = datetime.fromisoformat(ts)
        elif isinstance(ts, datetime):
            timestamp = ts
        else:
            timestamp = datetime.now(timezone.utc)

        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)

        level = str(payload.get("level", "INFO")).upper()
        if level not in {item.value for item in LogLevel}:
            level = LogLevel.INFO.value

        metadata = payload.get("metadata") or {}
        tags = {
            "severity_score": 3 if level == "ERROR" else 2 if level == "WARNING" else 1,
            "source": "api",
        }

        return {
            "timestamp": timestamp,
            "service": str(payload.get("service", "unknown-service")),
            "level": level,
            "message": str(payload.get("message", "")),
            "metadata_json": metadata,
            "tags_json": tags,
        }
