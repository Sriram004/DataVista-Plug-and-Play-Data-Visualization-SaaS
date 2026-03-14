from datetime import datetime

from pydantic import BaseModel, Field

from app.models.entities import AlertChannel, LogLevel


class LogIngestRequest(BaseModel):
    timestamp: datetime
    service: str = Field(min_length=2, max_length=120)
    level: LogLevel
    message: str = Field(min_length=1, max_length=5000)
    metadata: dict = Field(default_factory=dict)


class LogIngestResponse(BaseModel):
    accepted: bool
    log_id: int
    normalized_level: LogLevel


class LogSearchResponse(BaseModel):
    id: int
    timestamp: datetime
    service: str
    level: LogLevel
    message: str
    metadata_json: dict
    tags_json: dict

    class Config:
        from_attributes = True


class AlertRuleCreate(BaseModel):
    name: str
    service: str = "*"
    level: LogLevel = LogLevel.ERROR
    threshold: int = 50
    window_minutes: int = 5
    channel: AlertChannel = AlertChannel.DASHBOARD


class AlertRuleOut(BaseModel):
    id: int
    name: str
    service: str
    level: LogLevel
    threshold: int
    window_minutes: int
    channel: AlertChannel
    is_active: bool

    class Config:
        from_attributes = True


class AlertEventOut(BaseModel):
    id: int
    rule_id: int
    triggered_at: datetime
    message: str
    payload_json: dict

    class Config:
        from_attributes = True
