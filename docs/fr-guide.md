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

**Resources:**
- [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) — official FastAPI docs, start here
- [A Guide to Authentication in FastAPI with JWT](https://davidmuraya.com/blog/fastapi-jwt-authentication/) — full walkthrough, register/login/protected routes
- [Login & Registration System with JWT in FastAPI](https://www.geeksforgeeks.org/python/login-registration-system-with-jwt-in-fastapi/) — practical CRUD-style example

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

**Resources:**
- [TMDB API documentation](https://developer.themoviedb.org/reference/intro/getting-started) — the source you're proxying
- [httpx documentation — Timeouts](https://www.python-httpx.org/advanced/timeouts/) — official httpx docs on client/request timeouts
- [FastAPI and Redis Tutorial: Build a High-Performance Python API](https://redis.io/tutorials/develop/python/fastapi/) — official Redis tutorial, covers caching an external API's response

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

**Resources:**
- [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) — official FastAPI + SQLAlchemy tutorial
- [The Ultimate FastAPI Tutorial Part 7 — Database Setup with SQLAlchemy and Alembic](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/) — well-regarded series, this part covers exactly your migrations setup
- [Patterns and Practices for using SQLAlchemy 2.0 with FastAPI](https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy) — modern `Mapped`/`mapped_column` style, matches what's already in this repo

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

**Resources:**
- [FastAPI RBAC - Full Implementation Tutorial](https://www.permit.io/blog/fastapi-rbac-full-implementation-tutorial) — thorough walkthrough of the `RoleChecker`-as-dependency pattern
- [Role-based access control using FastAPI](https://dev.to/moadennagi/role-based-access-control-using-fastapi-h59) — shorter, practical example
- [FastAPI/Python Code Sample: API Role-Based Access Control](https://developer.auth0.com/resources/code-samples/api/fastapi/basic-role-based-access-control) — Auth0's reference sample, good for comparing your own approach against

---

## Cross-cutting concepts (show up in NFRs and Redis section too)

- **Redis caching**: cache-aside pattern, TTL/expiry, cache invalidation ("there are only two hard things in computer science...").
- **Rate limiting**: fixed window vs sliding window, why track failed logins by email in Redis instead of in Postgres.
- **Testing**: mocking an external HTTP call (don't let your tests hit real TMDB), FastAPI's `TestClient`, test database isolation.
- **Migrations**: why hand-written `CREATE TABLE` breaks reproducibility, what `alembic revision --autogenerate` actually detects vs. what it misses.
- **Structured logging**: why `print()` doesn't scale, what a log line needs to be useful in production (timestamp, level, context).

**Resources for the cross-cutting stuff:**
- [Redis Cache Aside Pattern Explained](https://parottasalna.hashnode.dev/redis-cache-aside-pattern) — short, clear explainer
- [Rate Limiting for Your FastAPI App](https://upstash.com/docs/redis/tutorials/python_rate_limiting) — Upstash's tutorial, directly applicable to your login rate-limit requirement
- [How to rate limit FastAPI with Redis](https://dev.to/dpills/how-to-rate-limit-fastapi-with-redis-1dhf) — concrete Redis `INCR` + expiry example
- [Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/) — official FastAPI docs on testing async endpoints
- [Developing and Testing an Asynchronous API with FastAPI and Pytest](https://testdriven.io/blog/fastapi-crud/) — TestDriven.io, a full CRUD + test suite example worth studying end to end
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) — widely-cited GitHub repo on structuring a FastAPI project past toy-app size
- [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template) — the official template; its `app/` folder is a good reference for how a "real" auth + Postgres + Docker FastAPI project is laid out

Look these up, understand the *why*, then write the code yourself.
