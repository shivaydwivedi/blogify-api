# Blogify API Architecture

## Overview

Blogify API is organized as a modular Django REST Framework application. The codebase follows a modular monolith structure with clear app boundaries, shared framework utilities, and production-ready infrastructure concerns separated from domain behavior.

The architecture is intentionally simple: HTTP clients interact with versioned REST APIs, API views delegate validation and persistence to Django/DRF components, domain models remain inside feature apps, asynchronous work is delegated to Celery, PostgreSQL is the source of truth, Redis supports background processing, and provider integrations are configured through environment variables.

## System Context

```mermaid
flowchart TD
    Client["Web / Mobile / API Client"] --> API["Blogify REST API"]
    API --> PostgreSQL["PostgreSQL / Neon"]
    API --> Redis["Redis / Upstash"]
    API --> Cloudinary["Cloudinary Media Storage"]
    API --> SMTP["Brevo SMTP"]
    API --> Admin["Django Admin"]
    Worker["Celery Worker"] --> Redis
    Worker --> PostgreSQL
    Worker --> SMTP
```

## Runtime Components

| Component | Responsibility |
| --- | --- |
| `config` | Settings, URL routing, WSGI/ASGI, Celery application wiring |
| `apps/accounts` | Custom user model, JWT auth, registration, email verification |
| `apps/posts` | Post publishing workflow, post visibility, filtering, search |
| `apps/content` | Categories and tags |
| `apps/comments` | Comments and one-level replies |
| `apps/likes` | Post likes and unlike behavior |
| `apps/bookmarks` | User bookmark management |
| `apps/notifications` | Notification model, creation services, read APIs |
| `apps/common` | Shared API response, exception, permission, pagination, model, and utility foundations |
| `apps/core` | Health check, infrastructure tasks, startup management commands |

## Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant URLConf
    participant View
    participant Serializer
    participant Permission
    participant Model
    participant DB as PostgreSQL
    Client->>URLConf: HTTP request
    URLConf->>View: Route to API view/viewset
    View->>Permission: Validate access
    View->>Serializer: Validate request / serialize response
    Serializer->>Model: Read or mutate domain object
    Model->>DB: Query or persist data
    DB-->>Model: Result
    Model-->>Serializer: Domain object
    Serializer-->>View: Response data
    View-->>Client: JSON response envelope
```

## Architectural Characteristics

- Modularity through Django app boundaries.
- Predictable REST endpoints under `/api/v1/`.
- PostgreSQL as source of truth.
- Redis-backed background task infrastructure.
- Explicit production configuration through environment variables.
- Clear separation between public API, admin UI, background jobs, and provider integrations.
- Testability through reusable common framework components and pytest coverage.

## Design Constraints

- The application is a modular monolith, not a microservice system.
- GraphQL, CQRS, event sourcing, Kubernetes, and distributed service orchestration are intentionally excluded.
- Business behavior should stay inside feature apps and reusable services, not in deployment scripts.
- Provider-specific production settings must remain environment-driven.

## Related Documentation

- [02_System_Architecture.md](02_System_Architecture.md)
- [05_Implementation_Blueprint.md](05_Implementation_Blueprint.md)
- [adr/README.md](adr/README.md)
