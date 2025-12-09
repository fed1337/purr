# Lemur setup options

## Prerequisites

- Docker 20.10+
- Docker Compose v2.0+
- Node.js 18+ and npm

## Build locally

### Python package

```shell
uv build
```

### Docs

Note: python-ldap from requirements breaks due to readthedocs.io not having the correct header files.  
The `make up-reqs` will update all requirement text files, and forcibly remove `python-ldap` from `requirements-docs.txt`.  
However, dependabot doesn't use `make up-reqs`, so we have to replicate the necessary dependencies here.  Without including these dependencies, the docs are unable to include generated autodocs

```shell
uv export --group docs --no-hashes -o requirements-docs.txt
grep -v "python-ldap" requirements-docs.txt > tempreqs
mv tempreqs requirements-docs.txt
cd docs
make html
```

## Frontend

The frontend is an AngularJS 1.x application that needs to be compiled:

```bash
npm install                       # Install dependencies
npm run build_static              # Runs gulp build
gulp package --urlContextPath=""  # set correct path for proper URL generating to backend
```

## Build with Docker

### Python package

### Docs

### Frontend

## Run locally

### App

1. Supposed you have uv installed
1. Activate virtual environment `source .venv/bin/activate`
1. Install python dependencies: `uv sync`
1. Update initial config in `lemur.conf.py`
1. Create migrations: `uv run lemur -c /path/to/lemur.conf.py db init`
1. Apply migrations: `uv run lemur -c /path/to/lemur.conf.py db migrate`
1. Create admin user with login `lemur` and password `password`:` uv run lemur -c /path/to/lemur.conf.py init -p password`
1. Build frontend
1. Run app: `uv run lemur -c /path/to/lemur.conf.py start`
1. Access via browser: http://localhost:8000

#### Configure Lemur

Create a config file at `~/.lemur/lemur.conf.py`:

```python
# Database
SQLALCHEMY_DATABASE_URI = 'postgresql://lemur:lemur@localhost:5432/lemur'

# Required settings
SECRET_KEY = 'your-secret-key-here'
LEMUR_SECURITY_TEAM_EMAIL = 'security@example.com'

# Enable CORS for development
CORS = True
DEBUG = True
```

Or use environment variables:

```bash
export SQLALCHEMY_DATABASE_URI='postgresql://lemur:lemur@localhost:5432/lemur'
export SECRET_KEY='your-secret-key-here'
export LEMUR_SECURITY_TEAM_EMAIL='security@example.com'
```

### Tests

```bash
# Install test dependencies
uv sync --group tests

# Run tests
pytest

# With coverage
pytest --cov=lemur
```

## Run with Docker

### App

### Tests

## 🔧 Common Commands

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

### Database extension setup

```shell
docker exec lemur-postgres psql -U lemur -d lemur -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

```

### Database Migrations

Create a new migration:

```bash
# In container
docker-compose -f docker-compose.dev.yml exec lemur lemur db revision --autogenerate -m "description"

# Locally
lemur db revision --autogenerate -m "description"
```

Apply migrations:

```bash
lemur db upgrade
```

## 🧪 Smoke testing

```bash
# Test frontend
curl http://localhost:8000/
# Should return HTML content

# Test API
curl http://localhost:8000/api/1/healthcheck
# Should return: {"status":"ok"}

# Test static files
curl http://localhost:8000/scripts/main.js
# Should return JavaScript content
```

## 🐛 Troubleshooting

1. .env files are not supported
2. Review logs: `docker-compose -f docker-compose.dev.yml logs -f lemur`

### Database errors

```bash
# Ensure PostgreSQL is running
docker-compose -f docker-compose.dev.yml ps postgres

# Run migrations
docker-compose -f docker-compose.dev.yml exec lemur lemur db upgrade
```

### Frontend Build Fails

```bash
rm -rf node_modules bower_components .tmp
npm install
npm run build_static
```

### Python import errors after changing dependencies.

```bash
# With Docker
docker-compose -f docker-compose.dev.yml build --no-cache

# Locally with uv
uv sync --reinstall
```

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
