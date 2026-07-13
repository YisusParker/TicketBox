# Setup — Reviewass

Reproducir el entorno con Docker (Python 3.11 en la imagen; no uses el Python del host).

## Requisitos

- Docker + Docker Compose
- Una API key de TMDB (gratuita): https://www.themoviedb.org/settings/api

## Config

Crea `.env` en la raíz del repo:

```env
DATABASE_URL=postgresql://reviewass:reviewass@db:5432/reviewass
REDIS_URL=redis://redis:6379/0
SECRET_KEY=IMEKTKQ94CqBWqWgOue00JRn
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TMDB_API_KEY=tu-api-key-de-tmdb
TMDB_BASE_URL=https://api.themoviedb.org/3
```

## Arranque

Primera vez (o si cambias `Dockerfile` / `requirements.txt`):

```bash
docker compose up --build
```

Día a día (la imagen ya existe):

```bash
docker compose up
# o en segundo plano:
docker compose up -d
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

Servicios: app (`8000`), Postgres (`5432`), Redis (`6379`).

## Estado

```bash
docker compose ps
curl http://localhost:8000/health
```

## Migraciones

Con los contenedores arriba, una vez que definas tus propios modelos en `app/models/`:

```bash
docker compose exec app alembic -c app/alembic.ini revision --autogenerate -m "mensaje"
docker compose exec app alembic -c app/alembic.ini upgrade head
```

## Parar

```bash
docker compose down
```

Conserva los datos de Postgres. Para borrarlos también: `docker compose down -v`.

## Qué construir

Ver `/docs/README.md` para el plan completo (usuarios/auth, búsqueda de películas vía TMDB, reviews y ratings).
