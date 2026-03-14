# LogVista – Cloud-Based Log Analytics & Monitoring Platform

LogVista is a cloud-native, multi-tenant log analytics platform. It provides secure log ingestion APIs, real-time processing, searchable log storage, and rule-based alerting similar to Datadog/Splunk/Elastic patterns.

## Implemented Architecture

### 1) Log Ingestion Service
- `POST /api/v1/logs/ingest` accepts JSON logs.
- Request validation via Pydantic schema.
- API key authentication (`X-API-Key`).
- Built-in per-key rate limiting.

### 2) Log Processing Engine
- Normalizes timestamps and log levels.
- Extracts metadata and attaches tags.
- Classifies severity (`INFO`, `WARNING`, `ERROR`).
- Triggers alert-rule evaluation after ingestion.

### 3) Message Queue Layer
- Queue abstraction (`QueueService`) between ingestion and processing.
- Current implementation: in-memory FIFO (extensible to Kafka/RabbitMQ/Redis Streams).

### 4) Log Storage
- `LogEvent` entity stores parsed logs for indexed access by org, service, level, and timestamp.
- SQLAlchemy models are structured to be replaceable with OpenSearch/Elasticsearch for larger scale.

### 5) Search API
- `GET /api/v1/logs/search` with:
  - time range (`hours`)
  - `service`
  - `level`
  - keyword search (`message`)
  - pagination (`page`, `page_size`)

### 6) Alerting System
- `POST /api/v1/logs/alerts/rules` to create rules.
- `GET /api/v1/logs/alerts/rules` and `GET /api/v1/logs/alerts/events`.
- Rule format: threshold + window + channel (`dashboard`, `email`, `webhook`).

### 7) Authentication & Security
- JWT auth for users.
- RBAC roles: `admin`, `developer`, `analyst`, `viewer`.
- API key authentication for ingestion clients.

## Quick Start
```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## API Flow Example
1. Register/Login and obtain JWT.
2. Create ingestion key (admin):
   - `POST /api/v1/logs/bootstrap-api-key?label=prod&raw_key=<your-secret-key>`
3. Send logs with `X-API-Key`:
   - `POST /api/v1/logs/ingest`
4. Query logs via JWT:
   - `GET /api/v1/logs/search?service=auth-service&level=ERROR&hours=24`
5. Configure alerts:
   - `POST /api/v1/logs/alerts/rules`

## Notes
- The queue/storage layers are intentionally modular so Kafka/OpenSearch/ClickHouse can be integrated without API breakage.
- Frontend dashboard integration can consume `/logs/search` and `/logs/alerts/events` for real-time charts and health indicators.
