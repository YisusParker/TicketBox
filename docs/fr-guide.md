# Functional Requirements Guide — What to Research

This is not a how-to. For every requirement in `docs/README.md` §3, it lists the **concepts** behind it and **search terms** to look up so you can implement it yourself. If you find yourself pasting these terms into an LLM for the finished code instead of reading docs/tutorials, you're skipping the part that teaches you something.

---

## FR-1: Users & Authentication

**Concepts:** password hashing vs. encryption, salts, JWT (structure: header/payload/signature), access tokens vs. refresh tokens, OAuth2 password flow, dependency injection, environment-based secrets.

**Search terms:**
- "why you never store plaintext passwords" / "bcrypt vs argon2"
- "passlib CryptContext bcrypt python"
- "FastAPI OAuth2PasswordBearer tutorial"
- "JWT explained" (jwt.io is a good interactive reference)
- "python-jose encode decode JWT"
- "FastAPI Depends dependency injection"
- "SQLAlchemy Enum column type"
- "pydantic-settings BaseSettings env file"

**Questions to be able to answer:** Why hash instead of encrypt a password? What's inside a JWT and can anyone read it without the secret key? What happens if your `SECRET_KEY` leaks? Why is a "get current user" dependency better than checking auth in every route by hand?

---

## FR-2: Movie Search (TMDB Integration)

**Concepts:** consuming a third-party REST API, API keys as secrets, server-to-server calls vs. exposing keys to a client, HTTP timeouts, response-shape translation (don't just forward TMDB's raw JSON), error mapping.

**Search terms:**
- "why you should never expose an API key in frontend code"
- "httpx python client timeout example"
- "TMDB API search movie" (you already have the raw endpoint docs)
- "backend for frontend pattern" / "API proxy pattern"
- "mapping upstream API errors to your own error format"
- "pydantic response model FastAPI"

**Questions to be able to answer:** Why does your API return a *simplified* shape instead of forwarding TMDB's response verbatim? What should happen if TMDB is down or slow — should your whole API hang? What's the difference between a client-side timeout and a server-side one?

---

## FR-3: Reviews & Ratings

**Concepts:** foreign keys and relationships, composite unique constraints, one-to-many, pagination (offset/limit), SQL aggregate functions, request/response schema validation.

**Search terms:**
- "SQLAlchemy ForeignKey relationship one to many"
- "SQLAlchemy UniqueConstraint multiple columns"
- "SQL AVG GROUP BY explained"
- "offset vs cursor pagination"
- "pydantic BaseModel request vs response schema"
- "SQLAlchemy Mapped mapped_column"

**Questions to be able to answer:** Why does the unique constraint need *both* `user_id` and `tmdb_movie_id`, not just one? What SQL would you write to get a movie's average rating without loading every review into Python first? Why validate the incoming `rating` is between 1 and 5 at the schema level instead of in the route function?

---

## FR-4: Authorization & User Control

**Concepts:** authentication vs. authorization (they are not the same thing), role-based access control (RBAC), ownership-based authorization, HTTP 401 vs 403, soft delete.

**Search terms:**
- "authentication vs authorization difference"
- "role based access control (RBAC) explained"
- "ownership-based authorization API"
- "HTTP status code 401 vs 403 when to use each"
- "soft delete vs hard delete database pattern"
- "FastAPI reusable Depends for role checks"

**Questions to be able to answer:** A logged-in `user` tries to delete someone else's review — is that a 401 or a 403, and why? Why deactivate (`is_active=false`) a user instead of deleting their row? Where should the ownership check live so you don't copy-paste it into every route?

---

## Cross-cutting concepts (show up in NFRs and Redis section too)

- **Redis caching**: cache-aside pattern, TTL/expiry, cache invalidation ("there are only two hard things in computer science...").
- **Rate limiting**: fixed window vs sliding window, why track failed logins by email in Redis instead of in Postgres.
- **Testing**: mocking an external HTTP call (don't let your tests hit real TMDB), FastAPI's `TestClient`, test database isolation.
- **Migrations**: why hand-written `CREATE TABLE` breaks reproducibility, what `alembic revision --autogenerate` actually detects vs. what it misses.
- **Structured logging**: why `print()` doesn't scale, what a log line needs to be useful in production (timestamp, level, context).

Look these up, understand the *why*, then write the code yourself.
