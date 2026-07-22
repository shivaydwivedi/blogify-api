# Contributing

## Development Principles

Contributions should preserve the existing modular Django architecture, shared common framework, explicit permissions, consistent response envelope, and production deployment behavior.

## Local Setup

```bash
python -m venv .venv
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
```

## Quality Gates

Run before submitting changes:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
pytest
black --check .
isort --check-only .
flake8 .
```

## Contribution Rules

- Do not introduce business behavior into deployment scripts.
- Do not bypass the shared response and exception framework.
- Do not add endpoints without OpenAPI documentation coverage.
- Do not change public API behavior without updating documentation.
- Keep migrations intentional and reviewable.
- Prefer clear, explicit code over hidden framework magic.

## Pull Request Checklist

- The change is scoped and explained.
- Tests cover new behavior.
- Documentation is updated.
- Formatting, imports, linting, and tests pass.
- Deployment implications are documented when relevant.
