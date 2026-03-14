from collections import deque


class QueueService:
    """Simple in-memory queue abstraction for decoupled ingestion/processing."""

    _queue: deque[dict] = deque()

    @classmethod
    def enqueue(cls, payload: dict) -> None:
        cls._queue.append(payload)

    @classmethod
    def dequeue(cls) -> dict | None:
        if not cls._queue:
            return None
        return cls._queue.popleft()
