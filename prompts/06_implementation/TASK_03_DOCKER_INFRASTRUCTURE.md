# TASK 03 — Docker Infrastructure

You are a Senior Platform Engineer responsible for containerizing Blogify API.

Before implementing anything, review and respect every approved engineering document:

- MASTER_CONTEXT.md
- PROJECT_CONTEXT.md
- PHASE_00_CONTEXT.md
- Project Vision
- PRD
- System Architecture
- Database Design
- API Design
- Implementation Blueprint
- Development Roadmap
- Coding Standards
- All ADRs

Treat them as mandatory engineering constraints.

---

# Objective

Implement the Docker infrastructure required for local development.

The result should provide a consistent, reproducible development environment.

---

# Scope

Implement ONLY:

## Dockerfile

Use a production-quality Dockerfile.

Optimize build layers.

Minimize image size.

Use Python 3.12.

---

## docker-compose.yml

Configure:

Django

PostgreSQL

Redis

Named volumes

Bridge network

Environment variables

Health checks

---

## docker-compose.prod.yml

Provide production overrides.

Do not configure deployment yet.

---

## .dockerignore

Exclude unnecessary files.

---

## entrypoint.sh

Responsibilities:

Wait for PostgreSQL.

Run migrations.

Start Django development server.

Keep the script simple and maintainable.

---

## Environment

Wire containers to the existing configuration layer.

Reuse .env.

Do not duplicate configuration.

---

# Constraints

Do NOT implement:

Celery

Celery Beat

Gunicorn

Nginx

Authentication

Business logic

Swagger URLs

Health endpoint

Models

Views

API endpoints

---

# Quality Expectations

The infrastructure should:

- Be production-oriented
- Be easy to understand
- Minimize duplication
- Follow Docker best practices
- Support future expansion

---

# Verification

Verify:

✓ docker compose config

✓ docker compose build

✓ docker compose up

✓ Django starts successfully

✓ PostgreSQL is reachable

✓ Redis is reachable

Document any assumptions.

---

# Pull Request Summary

Provide:

1. Summary of changes

2. Files added

3. Files modified

4. Verification performed

5. Risks

6. Future work

7. Suggested commit message