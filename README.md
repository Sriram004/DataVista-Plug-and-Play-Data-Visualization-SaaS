# DataVista – Plug-and-Play Data Visualization SaaS

DataVista is a cloud-native, multi-tenant analytics platform scaffold designed for production-grade evolution. It enables organizations to ingest data, build interactive dashboards, and enforce role-based access.

## Tech Stack
- **Frontend:** Next.js + React + ECharts
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL
- **Cache/Realtime Foundation:** Redis
- **Deployment:** Docker + docker-compose
- **CI/CD:** GitHub Actions

## Implemented Capabilities
### 1) Authentication & Multi-Tenancy
- JWT token issuance for login/register
- Organization-scoped user registration
- Tenant-aware data access in dataset/dashboard APIs
- RBAC for `admin`, `analyst`, `viewer`
- Bcrypt password hashing

### 2) Data Ingestion Layer
- CSV/XLSX upload endpoint
- File size validation
- Null cleaning and preview generation
- Basic schema inference (`dtype`, non-null counts)

### 3) Data Processing Engine (Core)
- Aggregation utility with `sum`, `avg`, `count` + `group by`
- Extensible service layer for filtering/sorting/pagination
- Redis included for future caching hooks

### 4) Dashboard Builder
- Dashboard CRUD API foundation
- Next.js dashboard page with widget composition placeholder
- ECharts dynamic rendering sample

### 5) API Design (Layered)
- Routes (controllers): `app/api/v1`
- Services: business logic
- Models/Schemas for persistence and IO contracts

### 6) Database Design
Core entities:
- Organizations
- Users (role + org foreign key)
- Datasets (metadata JSON)
- Dashboards
- Widgets
- Subscription plans

### 7) DevOps
- Dockerfiles for backend/frontend
- `docker-compose.yml` for local full stack
- GitHub Actions CI pipeline

### 8) Advanced Readiness
Structure prepared for:
- WebSockets
- Audit logs
- Billing integration
- Usage tracking and analytics APIs

## Local Run
```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## API Examples
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/datasets/upload`
- `GET /api/v1/datasets`
- `POST /api/v1/dashboards`
- `GET /api/v1/dashboards`

## Suggested Next Steps
1. Add Alembic migrations and full indexing strategy.
2. Persist dataset rows in a columnar/query engine.
3. Implement OAuth (Google) and refresh tokens.
4. Add websocket-driven widget live updates.
5. Add Stripe billing and plan enforcement middleware.
