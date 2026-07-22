# Security

## Security Model

Blogify API uses Django's security foundations, JWT Bearer authentication, object-level authorization, environment-based secrets, and production-only security settings.

## Authentication

- JWT access tokens authenticate API requests.
- Refresh token rotation is enabled.
- Refresh tokens are blacklisted on logout and after rotation.
- Passwords are hashed using Django's password framework.
- Password validation is enforced during registration and password change.

## Authorization

- Public users can read published posts, categories, tags, comments, Swagger, schema, and health status.
- Authenticated users can create posts, comment, like, bookmark, and read notifications.
- Authors can manage their own posts and comments.
- Staff/admin users can manage taxonomy and moderate content.
- Notification access is restricted to the recipient.

## Secrets

Production secrets must be supplied through environment variables. Do not commit `.env` files or provider credentials.

Important secrets include:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `CLOUDINARY_URL`
- `EMAIL_HOST_PASSWORD`
- `DJANGO_SUPERUSER_PASSWORD`

## Production Settings

Production enables secure cookies, SSL redirect controls, HSTS controls, host validation, CSRF trusted origins, WhiteNoise static serving, Cloudinary storage, and SMTP email delivery.

## Reporting Security Issues

This repository does not currently define a private vulnerability disclosure process. Add a project-specific security contact before opening the project to external contributors.
