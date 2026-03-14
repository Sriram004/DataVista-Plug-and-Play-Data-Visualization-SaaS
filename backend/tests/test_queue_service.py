from app.services.queue_service import QueueService


def test_enqueue_dequeue_roundtrip() -> None:
    payload = {"hello": "world"}
    QueueService.enqueue(payload)
    assert QueueService.dequeue() == payload
