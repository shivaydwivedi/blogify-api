# Deployment Guide

## Target Platform

The production deployment target is Render Docker with:

- Neon PostgreSQL
- Upstash Redis
- Cloudinary
- Brevo SMTP
- Gunicorn
- WhiteNoise

## Docker Startup

The container entrypoint performs:

1. Wait for PostgreSQL.
2. Run `python manage.py migrate --noinput`.
3. Run `python manage.py bootstrap_superuser`.
4. Run `python manage.py collectstatic --noinput` in production.
5. Run `python manage.py check`.
6. Start `gunicorn config.wsgi:application`.

## Required Render Environment Variables

| Variable | Notes |
| --- | --- |
| `DJANGO_SETTINGS_MODULE=config.settings.production` | Required |
| `DJANGO_ENVIRONMENT=production` | Required |
| `DJANGO_SECRET_KEY` | Required secret |
| `DJANGO_ALLOWED_HOSTS` | Include Render hostname |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Include HTTPS Render origin |
| `DATABASE_URL` | Neon PostgreSQL URL |
| `REDIS_URL` | Upstash Redis URL |
| `CELERY_BROKER_URL` | Usually same as `REDIS_URL` |
| `CELERY_RESULT_BACKEND` | Usually same as `REDIS_URL` |
| `CLOUDINARY_URL` | Cloudinary connection URL |
| `EMAIL_HOST` | Brevo SMTP host |
| `EMAIL_PORT` | Usually `587` |
| `EMAIL_HOST_USER` | Brevo SMTP user |
| `EMAIL_HOST_PASSWORD` | Brevo SMTP key |
| `EMAIL_USE_TLS=True` | Recommended |
| `BLOGIFY_API_BASE_URL` | Production base URL |

## Optional Initial Admin Bootstrap

Render Free Docker does not provide shell access or one-off jobs. To create the first superuser during startup, set:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=<secure-password>
```

The command is idempotent. If any superuser already exists, it does nothing.

Remove these variables after the first successful admin login.

## Static and Media Files

WhiteNoise serves collected static files. Cloudinary stores production media uploads.

## Health Check

Configure Render health checks against:

```text
/health/
```

Healthy response:

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```
