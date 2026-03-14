from app.services.log_processing_service import LogProcessingService


def test_normalize_sets_severity_and_defaults() -> None:
    normalized = LogProcessingService.normalize(
        {
            "timestamp": "2026-03-14T12:00:00",
            "service": "auth-service",
            "level": "error",
            "message": "Login failed",
            "metadata": {"user_id": "U123"},
        }
    )

    assert normalized["level"] == "ERROR"
    assert normalized["service"] == "auth-service"
    assert normalized["metadata_json"]["user_id"] == "U123"
    assert normalized["tags_json"]["severity_score"] == 3
