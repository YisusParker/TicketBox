# Backend Project Plan — Jesus (Beginner Track)

**Project:** "TicketBox" — Event Ticketing & Checkout API
---

## 1. Objective

Build a REST API for a small event-ticketing platform where users can browse events, reserve seats, and "pay" for tickets through a fake payment gateway. The goal is to demonstrate solid fundamentals: clean project structure, correct HTTP semantics, relational data modeling, basic caching, and testable business logic.

---

## 2. Guard Rails (Non-Negotiable Constraints)

1. **Pick exactly ONE framework** and stick with it for the entire project:
   - Python → FastAPI (or Django REST Framework)
   - Node.js → NestJS
   - Go → Gin
2. **Database:** PostgreSQL only. No SQLite, no MongoDB, no "temporary" alternatives.
3. **Cache:** Redis only, and it must be used for at least the use cases listed in §6.
5. All infrastructure must run locally via **docker-compose** (app + Postgres + Redis).
6. **Migrations are mandatory** (Alembic / TypeORM migrations / golang-migrate). No `CREATE TABLE` by hand in psql.

---

## 3. Functional Requirements

### FR-1: Users
- Register (email + password, hashed with bcrypt/argon2).
- Login returning a JWT (access token only is fine at this level).
- Get own profile (`GET /me`) — authenticated.

### FR-2: Events
- CRUD for events (create/update/delete restricted to an `admin` role; seed one admin user).
- Event fields: name, description, venue, starts_at, total_capacity, price_cents, currency, status (`draft`, `published`, `cancelled`).
- Public listing endpoint with pagination (`GET /events?page=&limit=`) and filtering by date range and status.

### FR-3: Ticket Reservation
- Authenticated user reserves N tickets for an event (`POST /events/{id}/reservations`).
- A reservation holds tickets for **10 minutes**. If not paid within that window, the tickets return to the available pool.
- The system must never oversell: capacity checks must be race-safe (use a DB transaction with row locking — `SELECT ... FOR UPDATE` — and be prepared to explain why).

### FR-4: Fake Payment Gateway
You will build a **separate mock payment module/service** inside the same codebase (a `payments` module with its own routes, simulating an external provider):
- `POST /mock-gateway/charges` accepts `{ amount_cents, currency, card_number, reservation_ref }`.
- Behavior rules (deterministic, so it can be tested):
  - Card ending in `0000` → always **declined**.
  - Card ending in `9999` → responds after a 5-second delay (simulates timeout handling).
  - Any other card → **approved**, returns a fake `charge_id`.
- The main API consumes this gateway over HTTP (yes, HTTP call to itself/localhost — the point is to practice integrating an external provider: timeouts, error mapping, retries **are not** required at this level, but a timeout on the HTTP client is).

### FR-5: Checkout
- `POST /reservations/{id}/pay` with card details → calls the mock gateway → on success, reservation becomes a confirmed `order` with generated ticket codes (UUIDs).
- On decline, reservation stays active until it expires.
- `GET /orders` and `GET /orders/{id}` for the authenticated user.

---

## 4. Non-Functional Requirements

- **NFR-1:** All list endpoints paginated; default limit 20, max 100.
- **NFR-2:** Consistent JSON error format: `{ "error": { "code": "...", "message": "..." } }`.
- **NFR-3:** Correct HTTP status codes (201 on create, 409 on capacity conflict, 402 on payment declined, etc.).
- **NFR-4:** Minimum 10 automated tests, covering at least: registration/login, overselling prevention, payment decline path, reservation expiry.
- **NFR-5:** A `README.md` with setup instructions that work from a clean machine (`docker-compose up` + one migration command).
- **NFR-6:** Structured logging (JSON logs or at least consistent log lines) for every payment attempt.

---

## 5. Data Model (Minimum Entities)

You must deliver an **ERD diagram** and, if using classes, a **class diagram** (Mermaid or draw.io, committed to the repo under `/docs`).

Required entities (you may add fields, not remove):

- `users` (id, email unique, password_hash, role, created_at)
- `events` (id, name, description, venue, starts_at, total_capacity, price_cents, currency, status, created_at)
- `reservations` (id, user_id, event_id, quantity, status [`pending`, `expired`, `paid`], expires_at, created_at)
- `orders` (id, reservation_id, user_id, amount_cents, currency, gateway_charge_id, created_at)
- `tickets` (id, order_id, event_id, code UUID, created_at)

Referential integrity enforced with real foreign keys. Explain your indexing choices for at least 2 indexes beyond primary keys.

---

## 6. Redis — Required Uses

1. **Event listing cache:** cache the published-events list for 60 seconds; invalidate on event create/update/delete. Be ready to explain cache invalidation choice.
2. **Reservation expiry:** either (a) a Redis key with TTL + a background sweep, or (b) a scheduled job checking `expires_at`. Justify your choice in the README.
3. **Login rate limiting:** max 5 failed logins per email per 15 minutes, tracked in Redis.

---

## 7. Deliverables Checklist

- [ ] Git repository with meaningful commit history (no single "final commit").
- [ ] `docker-compose.yml` (app, Postgres, Redis).
- [ ] Migrations folder.
- [ ] `/docs/erd.md` (ERD diagram) and `/docs/architecture.md` (module layout + request flow for the checkout: reservation → gateway → order, as a sequence diagram).
- [ ] OpenAPI/Swagger available at `/docs` endpoint (FastAPI/NestJS give this nearly free; Gin: use swaggo).
- [ ] Test suite runnable with a single command.
- [ ] Postman/Insomnia collection or `.http` file to exercise the full happy path.
- [ ] README: setup, design decisions, known limitations.

### Rubric (100 pts)
- Correctness of requirements — 30
- Data modeling & migrations — 15
- Concurrency safety (no overselling) — 15
- Code organization & readability — 15
- Tests — 10
- Redis usage & justification — 10
- Docs & diagrams — 5

