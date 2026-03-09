# ✅ TaskFlow API

A production-ready RESTful Task Management API built with **FastAPI**, featuring JWT authentication, full CRUD operations, filtering, pagination, and a Dockerised deployment.

> **Tech Stack:** Python · FastAPI · SQLAlchemy · SQLite/PostgreSQL · JWT · Docker · Pytest

---

## 🎯 What This Project Demonstrates

| Skill | How It's Shown |
|-------|---------------|
| REST API Design | Clean resource-based routes, proper HTTP verbs/status codes |
| Authentication | JWT access tokens + refresh token rotation |
| ORM + Database | SQLAlchemy models, migrations via Alembic |
| Input Validation | Pydantic schemas with custom validators |
| Testing | 90%+ coverage with pytest + TestClient |
| Docker | Multi-stage Dockerfile, docker-compose setup |
| Documentation | Auto-generated Swagger UI at `/docs` |

---

## 📂 Project Structure

```
taskflow-api/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── config.py         # Settings (pydantic-settings)
│   ├── database.py       # SQLAlchemy engine + session
│   ├── models/
│   │   ├── user.py       # User ORM model
│   │   └── task.py       # Task ORM model
│   ├── schemas/
│   │   ├── user.py       # Request/response schemas
│   │   └── task.py       # Task schemas with validators
│   ├── routers/
│   │   ├── auth.py       # /auth/register, /auth/login, /auth/refresh
│   │   └── tasks.py      # /tasks CRUD endpoints
│   └── utils/
│       ├── auth.py       # JWT creation + verification
│       └── hashing.py    # bcrypt password hashing
├── tests/
│   ├── conftest.py       # Test fixtures (DB, client, auth headers)
│   ├── test_auth.py
│   └── test_tasks.py
├── alembic/              # DB migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Option A: Docker (Recommended)

```bash
git clone https://github.com/canutex7/taskflow-api.git
cd taskflow-api
docker-compose up --build
```

API available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### Option B: Local

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

---

## 🔐 Authentication Flow

```
POST /auth/register   → Create user account
POST /auth/login      → Returns { access_token, refresh_token }
POST /auth/refresh    → Rotates refresh token → new access_token
```

All `/tasks` endpoints require `Authorization: Bearer <access_token>` header.

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/tasks` | List tasks (filter, sort, paginate) |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{id}` | Get task by ID |
| PATCH | `/tasks/{id}` | Update task fields |
| DELETE | `/tasks/{id}` | Delete a task |

### Query Parameters for `GET /tasks`

```
?status=pending|in_progress|done
?priority=low|medium|high
?due_before=2025-12-31
?sort=due_date|created_at
?order=asc|desc
?page=1&limit=20
```

---

## 📝 Example Usage

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "canute@example.com", "password": "Secret123!"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -d '{"username": "canute@example.com", "password": "Secret123!"}'

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deploy to production",
    "description": "Final deployment checklist",
    "priority": "high",
    "due_date": "2025-12-15"
  }'

# List tasks with filters
curl http://localhost:8000/tasks?status=pending&priority=high&sort=due_date \
  -H "Authorization: Bearer <token>"
```

---

## 🧱 Data Models

```python
# Task Schema
{
  "id": 1,
  "title": "Deploy to production",
  "description": "Final deployment checklist",
  "status": "pending",          # pending | in_progress | done
  "priority": "high",           # low | medium | high
  "due_date": "2025-12-15",
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-01T10:00:00Z",
  "owner_id": 42
}
```

---

## 🧪 Tests

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Test coverage includes: registration validation, duplicate email rejection, login flow, token expiry, task CRUD, ownership enforcement, filtering logic.

---

## 🐳 Docker Setup

```yaml
# docker-compose.yml (excerpt)
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/taskflow
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: taskflow
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

---

## 📦 Requirements

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
httpx==0.25.2
```

---

## 👨‍💻 Author

**Canute Fernandes** — [canutef7@gmail.com](mailto:canutef7@gmail.com) · [LinkedIn](https://linkedin.com/in/canutef)
