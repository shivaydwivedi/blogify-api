# Blogify API

Production-oriented REST API for a modern blogging platform.

## Requirements

- Python 3.12+
- PostgreSQL for production-like environments

## Local Setup

Create and activate a virtual environment, then install development dependencies:

```bash
pip install -r requirements/development.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Run Django checks:

```bash
python manage.py check
```

## Settings

The project uses a split settings package:

- `config.settings.base`
- `config.settings.development`
- `config.settings.production`
- `config.settings.testing`

Set `DJANGO_SETTINGS_MODULE` to select the environment.

Configuration is loaded from environment variables, with `.env` supported for
local development. Development and testing settings provide safe defaults.
Production settings validate required secrets, allowed hosts, and database
configuration at import time.

Important variables:

- `DJANGO_SETTINGS_MODULE`
- `DJANGO_ENVIRONMENT`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_LOG_LEVEL`
- `DJANGO_SECURITY_LOG_LEVEL`
- `DJANGO_ENABLE_FILE_LOGGING`
- `DJANGO_LOG_FILE_PATH`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_CONN_MAX_AGE`

Logging uses structured key-value console output by default. File logging is
available through `DJANGO_ENABLE_FILE_LOGGING=True`, but console logging remains
the default because it works cleanly with containers and process managers.

## Documentation

Architecture, product, database, API, implementation, and ADR documentation lives in `docs/`.
