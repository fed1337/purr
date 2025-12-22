# Lemur

Lemur manages TLS certificate creation. While not able to issue certificates itself, Lemur acts as a broker between CAs
and environments, providing a central portal for developers to issue TLS certificates with 'sane' defaults.

Lemur aims to support three of the most recent python releases which have been released for at least a year. For
example, if python 3.13 released last month, we'd aim to support versions 3.10, 3.11, and 3.12.

# Build & run

## Local

### Frontend

Build

```bash
npm install                       # Install dependencies
gulp build                        # Compiles frontend
gulp package --urlContextPath=""  # Sets correct base path to API endpoints
```

Run

```
gulp serve
```

### Backend

1. Supposed you have uv installed
2. Activate virtual environment: `source .venv/bin/activate`
3. Install python dependencies: `uv sync`
4. Review initial config in `lemur.conf.py` and adjust it to your needs
5. Make sure you are inside lemur package (with the migrations folder): `cd lemur/`
6. Create admin user with login `lemur` and password `password`:
   `uv run lemur -c /path/to/lemur.conf.py init -p password`
7. Run app: `uv run lemur -c /path/to/lemur.conf.py start`
8. Access via browser: http://localhost:8000

### Tests

```bash
# Install test dependencies
uv sync --group tests

# Run tests
pytest

# With coverage
pytest --cov=lemur
```

### Docs


## Docker

### Build

### Docker-compose

```bash
docker compose up -d postgres       # run postgres in background
docker compose run --rm lemur init  # initialize database (one time)
docker compose up -d lemur          # start the app
```

### Running tests

### Docker Development

```bash
# Start services
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f lemur

# Stop services
docker-compose -f docker-compose.dev.yml down

# Rebuild after code changes
docker-compose -f docker-compose.dev.yml up --build

# Run database migrations
docker-compose -f docker-compose.dev.yml exec lemur lemur db upgrade

# Access Python shell
docker-compose -f docker-compose.dev.yml exec lemur lemur shell
```

### Hot Reload

The development docker-compose includes `--reload` flag for gunicorn, so Python changes are automatically detected.


## Production environment overview

```
┌─────────────────────────────────────────────────────┐
│                   Browser/Client                    │
└─────────────────────┬───────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────┐
│     Caddy/your favorite web server (port 80/433)    │
│  • Serves static files (CSS, JS, images)            │
│  • Proxies /api/* to Flask backend                  │
│  • SPA routing (all routes → index.html)            │
└─────────────────────┬───────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────┐
│           Flask + Gunicorn (port 8000)              │
│  • REST API endpoints (/api/1/*)                    │
│  • Serves index.html for root route                 │
│  • SQLAlchemy ORM                                   │
└─────────┬───────────────────────────┬───────────────┘
          │                           │
          ↓                           ↓
┌──────────────────┐        ┌──────────────────┐
│   PostgreSQL     │        │      Redis       │
│   (port 5432)    │        │   (port 6379)    │
│  • Main database │        │  • Cache/Queue   │
│  • pg_trgm ext   │        │  • Celery broker │
└──────────────────┘        └──────────────────┘
                                      │
                                      ↓
                            ┌──────────────────┐
                            │  Celery Worker   │
                            │ • Background     │
                            │   tasks          │
                            └──────────────────┘
```

---

**Happy certificate management! 🎉**
