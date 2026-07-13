# Backend Project Plan — Jesus (Beginner Track)

**Project:** "Reviewass" — Movie Review & Rating API
---

## 1. Objective

Build a REST API where users can search for movies (via the TMDB API), write reviews, and rate movies with stars. The goal is to demonstrate solid backend fundamentals: authentication, authorization, clean project structure, correct HTTP semantics, relational data modeling, basic caching, and testable business logic.

---

## 2. Guard Rails (Non-Negotiable Constraints)

1. **FastAPI**, Python. Stick with it for the entire project.
2. **Database:** PostgreSQL only. No SQLite, no MongoDB, no "temporary" alternatives.
3. **Cache:** Redis only, and it must be used for at least the use cases listed in §6.
4. All infrastructure must run locally via **docker-compose** (app + Postgres + Redis) — already scaffolded for you.
5. **Migrations are mandatory** (Alembic). No `CREATE TABLE` by hand in psql.
6. **Never store the TMDB API key client-side or return it in any response.** All TMDB calls happen server-to-server; your API is the only thing that talks to TMDB.

---

## 3. Functional Requirements

### FR-1: Users & Authentication
- Register (email + password, hashed with bcrypt).
- Login returning a JWT (access token only is fine at this level).
- Get own profile (`GET /me`) — authenticated.
- Update own profile (`PATCH /me`) — authenticated.
- Roles: `user` and `admin` (seed one admin user via a script or migration data).

### FR-2: Movie Search (TMDB Integration)
Get a free API key at https://www.themoviedb.org/settings/api and set `TMDB_API_KEY` in `.env` (already added to `app/config.py`'s `Settings`).

- `GET /movies/search?query=&page=` — proxies TMDB's `GET /search/movie` and returns a simplified shape (`tmdb_id`, `title`, `poster_path`, `release_date`, `vote_average`). Public, no auth required.
- `GET /movies/{tmdb_id}` — proxies TMDB's `GET /movie/{movie_id}` for details (overview, genres, runtime, poster). Public.
- Use `httpx` with an explicit timeout for all outbound TMDB calls. Map TMDB errors (404, rate limit, timeout) to sensible API error responses — don't leak raw TMDB error bodies.
- There is no local `movies` table — TMDB is the source of truth for movie data. Your `reviews` table only stores the `tmdb_movie_id`.

### FR-3: Reviews & Ratings
- `POST /movies/{tmdb_id}/reviews` — authenticated user creates a review: `rating` (1–5 stars, integer) + `body` (text). **One review per user per movie** — enforce with a unique constraint on `(user_id, tmdb_movie_id)`, return `409` on duplicate.
- `GET /movies/{tmdb_id}/reviews` — public, paginated list of reviews for a movie, plus the movie's average rating.
- `GET /reviews/{id}` — public, single review.
- `PATCH /reviews/{id}` / `DELETE /reviews/{id}` — only the review's owner (or an admin) may edit/delete it. Enforce this in code, not just in the UI.
- `GET /users/{id}/reviews` — public, paginated list of a given user's reviews.

### FR-4: Authorization & User Control
- Role-based access: `admin` can delete **any** review (moderation) and deactivate (`is_active = false`) any user account. Deactivated users cannot log in.
- Ownership checks on every mutating review endpoint: confirm `review.user_id == current_user.id` or `current_user.role == "admin"` before allowing edit/delete.
- Dependency-injected `get_current_user` and `require_admin` (FastAPI `Depends`) — don't repeat auth logic per-route.

---

## 4. Non-Functional Requirements

- **NFR-1:** All list endpoints paginated; default limit 20, max 100.
- **NFR-2:** Consistent JSON error format: `{ "error": { "code": "...", "message": "..." } }`.
- **NFR-3:** Correct HTTP status codes (201 on create, 409 on duplicate review, 401 on missing/invalid auth, 403 on forbidden ownership, 404 on missing resource).
- **NFR-4:** Minimum 10 automated tests, covering at least: registration/login, duplicate-review rejection, ownership enforcement on edit/delete, TMDB search response shape (mock the TMDB call in tests — don't hit the real API).
- **NFR-5:** A `README.md` with setup instructions that work from a clean machine (`docker-compose up` + one migration command).
- **NFR-6:** Structured logging (JSON logs or at least consistent log lines) for every outbound TMDB call and every failed login attempt.

---

## 5. Data Model (Minimum Entities)

You must deliver an **ERD diagram** and, if using classes, a **class diagram** (Mermaid or draw.io, committed to the repo under `/docs`).

Required entities (you may add fields, not remove):

- `users` (id, email unique, password_hash, role, is_active, created_at)
- `reviews` (id, user_id FK → users, tmdb_movie_id int, rating int 1–5, body, created_at, updated_at, unique on `(user_id, tmdb_movie_id)`)

Referential integrity enforced with real foreign keys. Explain your indexing choices for at least 2 indexes beyond primary keys (hint: you will query reviews by `tmdb_movie_id` a lot, and by `user_id` for the user's-reviews endpoint).

---

## 6. Redis — Required Uses

1. **Movie response cache:** cache TMDB search results and movie-details responses for 60 seconds per query/id, to avoid hammering TMDB and to survive their rate limits. Be ready to explain your cache key design (must vary by query string / page / movie id).
2. **Average rating cache:** cache a movie's average rating, invalidate on every new/edited/deleted review for that movie. Justify your invalidation strategy in the README.
3. **Login rate limiting:** max 5 failed logins per email per 15 minutes, tracked in Redis.

---

## 7. Deliverables Checklist

- [ ] Git repository with meaningful commit history (no single "final commit").
- [ ] `docker-compose.yml` (app, Postgres, Redis) — already provided, don't need to touch it.
- [ ] Migrations folder — you'll generate your first migration once your models exist.
- [ ] `/docs/erd.md` (ERD diagram) and `/docs/architecture.md` (module layout + request flow for: search → review creation → rating aggregation, as a sequence diagram).
- [ ] OpenAPI/Swagger available at `/docs` endpoint (FastAPI gives this nearly free).
- [ ] Test suite runnable with a single command.
- [ ] Postman/Insomnia collection or `.http` file to exercise the full happy path.
- [ ] README: setup, design decisions, known limitations.

### Rubric (100 pts)
- Correctness of requirements — 30
- Data modeling & migrations — 15
- Authorization correctness (ownership + roles, no leaking others' write access) — 15
- Code organization & readability — 15
- Tests — 10
- Redis usage & justification — 10
- Docs & diagrams — 5
