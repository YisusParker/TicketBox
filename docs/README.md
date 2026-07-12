# Setup — TicketBox

Reproducir el entorno con Docker (Python 3.11 en la imagen; no uses el Python del host).

## Requisitos

- Docker + Docker Compose

## Config

Crea `.env` en la raíz del repo:

```env
DATABASE_URL=postgresql://ticketbox:ticketbox@db:5432/ticketbox
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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

Con los contenedores arriba:

```bash
docker compose exec app alembic -c app/alembic.ini revision --autogenerate -m "mensaje"
docker compose exec app alembic -c app/alembic.ini upgrade head
```

## Parar

```bash
docker compose down
```

Conserva los datos de Postgres. Para borrarlos también: `docker compose down -v`.
