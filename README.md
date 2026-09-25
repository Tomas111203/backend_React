# ⚡ Backend Module: FastAPI REST API & PostgreSQL Database

This directory contains the **FastAPI** REST microservice, the **PostgreSQL** database definition for the `videogames` table, and the main Docker orchestration file **`docker-compose.yml`**.

---

## 📂 Module Contents

- **`docker-compose.yml`**: Main Docker Compose orchestrator file for the entire stack (`auth-ldap-oauth2`, `backend`, and `frontend`).
- **`app/main.py`**:
  - RESTful API featuring full CRUD operations for videogames (`/api/videogames`).
  - `CORSMiddleware` setup to handle cross-origin browser requests seamlessly.
  - JWT RS256 Bearer Token verification dynamically querying Keycloak's JWKS public endpoint (`/protocol/openid-connect/certs`).
  - Static file routing fallback to serve the compiled React SPA at `/app/static`.
- **`app/models.py` & `app/schemas.py`**: SQLAlchemy ORM models and Pydantic validation schemas.
- **`init.sql`**: SQL database initialization script creating the `videogames` table (Name + 5 Attributes: Genre, Platform, Release Year, Rating, Developer).
- **`Dockerfile`**: Python 3.11 Slim container build instructions.

---

## 🚀 Deployment Commands

From this directory (`backend/`):

```bash
# Start the complete lab stack
docker compose up -d --build

# View FastAPI microservice logs
docker compose logs -f videogames-api
```

---

## 🌐 Main Endpoints

- **Swagger / OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Healthcheck Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)
- **Videogames API Endpoint**: `GET`, `POST`, `PUT`, `DELETE` `/api/videogames`
