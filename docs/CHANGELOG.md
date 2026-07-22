# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project uses practical semantic versioning for documentation purposes.

## [Unreleased]

### Added

- World-class GitHub README.
- Public documentation set for architecture, API usage, deployment, contribution, security, and system design.
- Postman collection for core API workflows.

## [0.1.0] - 2026-07-22

### Added

- Custom user model.
- JWT authentication with refresh rotation and blacklist logout.
- Email verification with Celery-backed email delivery.
- Category and tag CRUD.
- Post CRUD with draft/published workflow.
- Comments with one-level replies.
- Likes and bookmarks.
- Notification system.
- Django Admin route and model registrations.
- Health endpoint.
- Docker and Render deployment support.
- Neon PostgreSQL, Upstash Redis, Cloudinary, Brevo SMTP, WhiteNoise, and Gunicorn configuration.
- Test suite covering core API behavior and production hardening.
