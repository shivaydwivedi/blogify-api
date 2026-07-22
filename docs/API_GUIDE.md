# Blogify API Guide

## Base URL

Use the deployed Render URL in production:

```text
https://your-render-service.onrender.com
```

Local development defaults to:

```text
http://localhost:8000
```

## Documentation URLs

| Resource | Path |
| --- | --- |
| Swagger UI | `/api/v1/docs/` |
| OpenAPI schema | `/api/v1/schema/` |
| Health check | `/health/` |
| Django Admin | `/admin/` |

## Authentication

Blogify uses JWT Bearer authentication.

```http
Authorization: Bearer <access_token>
```

Access tokens last 15 minutes. Refresh tokens last 7 days. Refresh token rotation and blacklisting are enabled.

## Standard Responses

Success responses use:

```json
{
  "data": {}
}
```

Paginated responses use:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_count": 0,
    "total_pages": 1,
    "next": null,
    "previous": null
  }
}
```

Error responses use:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed.",
    "details": {}
  }
}
```

## Authentication Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register/` | Register account |
| `POST` | `/api/v1/auth/login/` | Obtain JWT tokens |
| `POST` | `/api/v1/auth/refresh/` | Refresh JWT tokens |
| `POST` | `/api/v1/auth/logout/` | Blacklist refresh token |
| `GET` | `/api/v1/auth/me/` | Read current user |
| `PUT` | `/api/v1/auth/change-password/` | Change password |
| `POST` | `/api/v1/auth/resend-verification/` | Resend verification email |
| `GET` | `/api/v1/auth/verify-email/?token=...` | Verify email |

## Content Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/posts/` | List visible posts |
| `POST` | `/api/v1/posts/` | Create post |
| `GET` | `/api/v1/posts/{id}/` | Retrieve post |
| `PUT/PATCH` | `/api/v1/posts/{id}/` | Update post |
| `DELETE` | `/api/v1/posts/{id}/` | Delete post |
| `GET` | `/api/v1/categories/` | List categories |
| `GET` | `/api/v1/tags/` | List tags |

## Engagement Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/posts/{id}/comments/` | List comments |
| `POST` | `/api/v1/posts/{id}/comments/` | Create comment or reply |
| `PUT/PATCH` | `/api/v1/comments/{id}/` | Update comment |
| `DELETE` | `/api/v1/comments/{id}/` | Delete comment |
| `POST` | `/api/v1/posts/{id}/like/` | Like post |
| `DELETE` | `/api/v1/posts/{id}/like/` | Unlike post |
| `GET` | `/api/v1/bookmarks/` | List bookmarks |
| `POST` | `/api/v1/posts/{id}/bookmark/` | Bookmark post |
| `DELETE` | `/api/v1/posts/{id}/bookmark/` | Remove bookmark |

## Notifications

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/notifications/` | List notifications |
| `PATCH` | `/api/v1/notifications/{id}/read/` | Mark one read |
| `PATCH` | `/api/v1/notifications/read-all/` | Mark all read |

## Filtering and Pagination

Posts support `category`, `tag`, `author`, `status`, `featured`, `search`, `ordering`, `page`, and `page_size`.

Categories support `is_active`, `search`, `ordering`, `page`, and `page_size`.

Tags support `search`, `ordering`, `page`, and `page_size`.

## Uploads

Post images are uploaded through multipart form data using the `featured_image` field. In production, uploaded media is stored through Cloudinary.
