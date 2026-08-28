# FastAPI Todo API

A production-style REST API for task management, built with FastAPI — featuring JWT authentication, role-based access control, database migrations, and automated tests.

🔗 **Live demo (Swagger UI):** https://fastapi-todo-was8.onrender.com/docs

> Note: hosted on Render's free tier — the first request may take ~30 seconds to wake the service.

---

## Why this project

Built to practise the parts of backend engineering that matter in production, not just CRUD:
authentication and authorisation, ownership checks, schema migrations, automated testing, and real deployment.

---

## Features

| Area | What's implemented |
|---|---|
| **Auth** | User registration, OAuth2 password flow, JWT access tokens |
| **Authorisation** | Role-based access (`user` / `admin`); users can only modify their own todos |
| **Todos** | Full CRUD with Pydantic validation (title/description length, priority 1–5) |
| **User** | Change password (with old-password verification), update phone number |
| **Admin** | List all todos, delete any todo |
| **Ops** | `/healthy` health-check endpoint for uptime monitoring |
| **Data** | SQLAlchemy ORM + Alembic migrations |
| **Testing** | 20 pytest cases covering auth, ownership, validation and error paths |
| **Deployment** | Auto-deployed to Render on every push to `main` |

---

## Tech stack

**FastAPI** · **SQLAlchemy** · **Alembic** · **Pydantic** · **python-jose (JWT)** · **passlib (bcrypt)** · **pytest** · **Docker** · **Render**

---

## API overview

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/healthy` | — | Health check |
| `POST` | `/auth/` | — | Register a new user |
| `POST` | `/auth/token` | — | Log in, returns JWT |
| `GET` | `/todos/` | ✅ | List the current user's todos |
| `POST` | `/todos/` | ✅ | Create a todo |
| `GET` | `/todos/{id}` | ✅ | Get one todo (ownership enforced) |
| `PUT` | `/todos/{id}` | ✅ | Update a todo (ownership enforced) |
| `DELETE` | `/todos/{id}` | ✅ | Delete a todo (ownership enforced) |
| `GET` | `/user/` | ✅ | Get current user profile |
| `PUT` | `/user/` | ✅ | Change password |
| `PUT` | `/user/phone_number` | ✅ | Update phone number |
| `GET` | `/admin/todos` | 🔑 admin | List all todos |
| `DELETE` | `/admin/todos/{id}` | 🔑 admin | Delete any todo |

Full interactive docs: [`/docs`](https://fastapi-todo-was8.onrender.com/docs)

---

## Running locally

```bash
git clone https://github.com/RaizelLee/FastAPI_Todo.git
cd FastAPI_Todo
pip install -r requirements.txt

# create a .env file (see .env.example)
cp .env.example .env

uvicorn TodoApp.main:app --reload
```

Open http://localhost:8000/docs

### With Docker

```bash
docker build -t fastapi-todo .
docker run -p 8000:8000 --env-file .env fastapi-todo
```

### Running the tests

```bash
pytest -v
```

Tests run against an isolated test database, so your development data is untouched.

---

## Configuration

Secrets are read from environment variables — nothing sensitive is committed.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Key used to sign JWTs |
| `ALGORITHM` | JWT signing algorithm (e.g. `HS256`) |
| `DATABASE_URL` | Database connection string |

---

## Design decisions

- **Ownership enforced at the query level** — update and delete filter by `owner_id` rather than checking after fetching, so one user can never touch another user's data.
- **Role check as a dependency** — admin routes reject non-admin tokens before any handler logic runs.
- **Alembic over auto-create** — schema changes are versioned and reversible, the way they would be on a real team.
- **Health-check endpoint** — lets the platform detect a broken deploy instead of serving errors silently.

---

## Known limitations

- Uses SQLite; a production deployment would use PostgreSQL with a connection pool.
- No rate limiting or refresh-token rotation yet.
- No pagination on list endpoints — fine at this scale, would be needed with real volume.
- Free-tier hosting sleeps when idle, so the first request is slow.

---

## Roadmap

- [ ] GitHub Actions CI running the test suite on every pull request
- [ ] Migrate to PostgreSQL
- [ ] Pagination and filtering on list endpoints
- [ ] Structured logging and request tracing
