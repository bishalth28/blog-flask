# 📝 Blog Flask — REST API + Web Interface

A full-stack blogging application built with **Flask**, featuring JWT authentication, a REST API with Swagger UI documentation, SQLAlchemy ORM with Alembic migrations, and a Jinja2 frontend. Users can register, log in, and create, edit, and delete their own blog posts.

---

## 📌 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Running with Docker](#running-with-docker)
- [Database Migrations](#database-migrations)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Pages & Routes](#pages--routes)
- [Security Notice](#security-notice)

---

## Features

- **User registration & login** with password hashing (PBKDF2-SHA256)
- **JWT-based authentication** — protected routes require a Bearer token
- **Full CRUD for blog posts** — create, read, update, and delete
- **Ownership enforcement** — users can only edit/delete their own posts
- **Swagger UI** auto-generated from OpenAPI 3.0 spec at `/swagger-ui`
- **Flask-Migrate / Alembic** for version-controlled database migrations
- **CORS enabled** for cross-origin frontend access
- **Docker support** — single-command local deployment
- **SQLite by default**, configurable via `DATABASE_URL` environment variable

---

## Project Structure

```
blog-flask-main/
│
├── app.py                  # App factory — registers blueprints, JWT, DB, CORS
├── main.py                 # WSGI entry point
├── db.py                   # SQLAlchemy instance
├── schemas.py              # Marshmallow schemas (UserSchema, PostSchema)
├── requirements.txt        # Python dependencies
├── dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose service config
│
├── models/
│   ├── user.py             # UserModel — id, username, password
│   └── post.py             # PostModel — id, title, description, created_at, author_id
│
├── route/
│   ├── user.py             # /register, /login, /user/<id>, /dashboard, /blog
│   └── post.py             # /posts, /posts/<id> (CRUD)
│
├── templates/
│   ├── register.html       # Registration form
│   ├── login.html          # Login form
│   ├── dashboard.html      # User dashboard — lists own posts
│   └── blog.html           # Create post form
│
├── static/
│   └── styles.css          # Application styles
│
├── migrations/             # Alembic migration history
│   └── versions/
│       └── 27b954926cdd_initial_migration_with_usermodel_and_.py
│
└── instance/
    └── data.db             # SQLite database (auto-created)
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Web Framework | [Flask](https://flask.palletsprojects.com/) |
| ORM | [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) |
| Migrations | [Flask-Migrate](https://flask-migrate.readthedocs.io/) + Alembic |
| Authentication | [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) |
| API Docs | [Flask-Smorest](https://flask-smorest.readthedocs.io/) + OpenAPI 3.0 |
| Serialization | [Marshmallow](https://marshmallow.readthedocs.io/) |
| Password Hashing | [Passlib](https://passlib.readthedocs.io/) (PBKDF2-SHA256) |
| CORS | [Flask-CORS](https://flask-cors.readthedocs.io/) |
| Database | SQLite (default) / any SQLAlchemy-compatible DB |
| Containerization | Docker + Docker Compose |
| Language | Python 3.10+ |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/blog-flask.git
cd blog-flask
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
export JWT_SECRET_KEY="your-secure-secret-key"
export DATABASE_URL="sqlite:///data.db"    # or a PostgreSQL URL
```

### 5. Run database migrations

```bash
flask --app app:create_app db upgrade
```

### 6. Start the development server

```bash
python main.py
```

The app will be available at **http://localhost:5000**

Swagger UI (API docs): **http://localhost:5000/swagger-ui**

---

## Running with Docker

### Single command startup

```bash
docker-compose up --build
```

The app starts on **http://localhost:5000**.

### docker-compose.yml overview

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app              # live reload during development
    environment:
      - FLASK_ENV=development
```

### Dockerfile overview

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

To use a persistent external database (e.g. PostgreSQL) with Docker, add a `DATABASE_URL` to the `environment` section in `docker-compose.yml`.

---

## Database Migrations

Flask-Migrate manages schema changes using Alembic under the hood.

```bash
# Apply all pending migrations to the database
flask --app app:create_app db upgrade

# Create a new migration after changing a model
flask --app app:create_app db migrate -m "describe your change"

# Roll back the last migration
flask --app app:create_app db downgrade
```

### Database Schema

**users**
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Unique |
| password | String(80) | Not Null (hashed) |

**post_model**
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| title | String(120) | Not Null |
| description | Text | Not Null |
| created_at | DateTime | Default: now |
| author_id | Integer | FK → users.id |

---

## API Reference

Full interactive docs are available at **`/swagger-ui`** when the app is running.

### Auth Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | ❌ | Register a new user |
| `POST` | `/login` | ❌ | Log in and receive a JWT access token |
| `GET` | `/user/<id>` | ✅ JWT | Get user details by ID |
| `DELETE` | `/user/<id>` | ✅ JWT | Delete a user by ID |

### Post Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/posts` | ❌ | List all blog posts |
| `POST` | `/posts` | ✅ JWT | Create a new post (as the authenticated user) |
| `GET` | `/posts/<id>` | ❌ | Get a single post by ID |
| `PUT` | `/posts/<id>` | ✅ JWT | Update a post (owner only) |
| `DELETE` | `/posts/<id>` | ✅ JWT | Delete a post (owner only) |

### Request & Response Examples

**Register**
```http
POST /register
Content-Type: application/json

{
  "username": "alice",
  "password": "securepassword"
}
```
```json
{ "message": "User created successfully" }
```

**Login**
```http
POST /login
Content-Type: application/json

{
  "username": "alice",
  "password": "securepassword"
}
```
```json
{ "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." }
```

**Create Post** (requires token)
```http
POST /posts
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My First Post",
  "description": "Hello, world!"
}
```
```json
{
  "id": 1,
  "title": "My First Post",
  "description": "Hello, world!",
  "created_at": "2025-08-03T17:59:56",
  "author_id": 1
}
```

---

## Authentication Flow

```
1. User submits credentials to POST /login
         │
         ▼
2. Server verifies password hash (PBKDF2-SHA256)
         │
         ▼
3. Server returns JWT access token
         │
         ▼
4. Client stores token in localStorage
         │
         ▼
5. Client sends token in Authorization header
   for all protected requests:
   Authorization: Bearer <token>
         │
         ▼
6. Flask-JWT-Extended validates token on each request
   get_jwt_identity() → returns the user's ID
```

**Ownership enforcement** — on `PUT /posts/<id>` and `DELETE /posts/<id>`, the server compares `post.author_id` with the identity from the JWT. A `403 Forbidden` is returned if they don't match.

---

## Pages & Routes

| URL | Template | Description |
|-----|----------|-------------|
| `/` | — | Redirects to `/login` |
| `/register` | `register.html` | Registration form |
| `/login` | `login.html` | Login form — stores JWT in `localStorage` |
| `/dashboard` | `dashboard.html` | Lists the logged-in user's posts |
| `/blog` | `blog.html` | Form to create a new post |

The frontend templates use vanilla JavaScript `fetch()` to call the REST API and store the JWT in `localStorage`. If no token is found, the user is redirected to `/login`.

---

## Security Notice

Before deploying to production, update the following:

**1. Change the JWT secret key**

In `app.py`, replace the hardcoded value with an environment variable:

```python
# ❌ Current (insecure)
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-in-production"

# ✅ Correct
import os
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
```

**2. Use a production database**

Set `DATABASE_URL` to a PostgreSQL or MySQL connection string instead of SQLite:

```bash
export DATABASE_URL="postgresql://user:password@host:5432/blogdb"
```

**3. Disable debug mode**

Ensure `debug=False` in production (already set in `main.py`).

**4. Add token expiry**

Configure JWT expiration in `app.py`:

```python
from datetime import timedelta
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
```

---

## Contributing

Ideas for extending the project:

- Add post pagination and search
- Add tags/categories to posts
- Add a public-facing post list page (no login required)
- Add profile pages per user
- Replace SQLite with PostgreSQL in Docker Compose
- Add refresh token support

