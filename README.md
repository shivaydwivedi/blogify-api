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

## Documentation

Architecture, product, database, API, implementation, and ADR documentation lives in `docs/`.
