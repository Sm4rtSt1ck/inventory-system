# University Equipment Inventory System

REST API for managing university department equipment inventory.

## Tech Stack

- Python 3.12, Django 5.x, Django REST Framework
- PostgreSQL
- JWT auth via `djangorestframework-simplejwt`
- OpenAPI/Swagger via `drf-spectacular`

## Setup

### 1. Clone and create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env — set DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY
```

### 3. Create PostgreSQL database

```sql
CREATE DATABASE university_equipment;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE university_equipment TO your_user;
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Seed the database

```bash
python manage.py seed_db
```

This creates:
- 3 laboratories
- 5 persons (2 lab managers, 3 teachers)
- 10 equipment items with components
- 10 assignments (active and historical)
- 3 users:
  | Username | Password    | Role        |
  |----------|-------------|-------------|
  | admin    | admin123    | admin       |
  | manager  | manager123  | lab_manager |
  | teacher  | teacher123  | teacher     |

### 6. Run the server

```bash
python manage.py runserver
```

## API Documentation

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI schema: http://localhost:8000/api/schema/

## API Endpoints

### Authentication — `/api/auth/`

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| POST | `/api/auth/login/` | Obtain JWT token pair | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| GET | `/api/auth/me/` | Current user info | Yes |
| POST | `/api/auth/register/` | Register new user | Admin only |

### Equipment — `/api/equipment/`

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| GET | `/api/equipment/` | List all (`?status=`, `?type=`, `?search=`) | Yes |
| POST | `/api/equipment/` | Create equipment | Admin |
| GET | `/api/equipment/{id}/` | Detail | Yes |
| PUT/PATCH | `/api/equipment/{id}/` | Update | Admin / Lab manager |
| DELETE | `/api/equipment/{id}/` | Delete | Admin |
| GET | `/api/equipment/{id}/components/` | List components | Yes |
| POST | `/api/equipment/{id}/components/` | Add component | Admin |
| DELETE | `/api/equipment/{id}/components/{comp_id}/` | Remove component | Admin |
| GET | `/api/equipment/{id}/history/` | Change history | Yes |

### Assignment — `/api/`

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| GET | `/api/laboratories/` | List laboratories | Yes |
| POST | `/api/laboratories/` | Create laboratory | Admin |
| GET | `/api/persons/` | List persons | Yes |
| POST | `/api/persons/` | Create person | Admin |
| GET | `/api/assignments/` | List (`?active=true/false`) | Yes |
| POST | `/api/assignments/` | Create assignment | Admin / Lab manager |
| PATCH | `/api/assignments/{id}/` | Update (e.g. close) | Admin / Lab manager |

## SOLID/DRY/KISS compliance

| Principle | Implementation |
|-----------|----------------|
| **SRP** | Each app handles one domain; serializers are split into read/write variants |
| **DRY** | History logging via Django signals (`equipment/signals.py`), permissions in `core/permissions.py` |
| **KISS** | Standard DRF ViewSets; no custom ORM beyond `filter()` |
| **OCP** | `IsAdmin`, `IsLabManager`, `IsAdminOrLabManager` are additive — views reference them without modification |
| **DIP** | Views depend on serializers and querysets (abstractions), not on concrete model queries |
