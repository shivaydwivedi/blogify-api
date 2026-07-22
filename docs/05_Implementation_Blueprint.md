# Blogify API - Implementation Blueprint

## 1. Executive Overview

This document defines the implementation strategy for Blogify API. It translates the approved product, architecture, database, and API design documents into practical engineering standards that guide day-to-day development.

The blueprint does not replace the Project Vision, PRD, System Architecture, Database Design, or API Design Specification. Those documents define why the system exists, what it must do, how it is organized, how data is modeled, and how consumers interact with the API. This document defines how engineers should implement the system while preserving those approved decisions.

Blogify API will be implemented as a modular monolith using layered architecture and Clean Architecture principles. The implementation must keep business logic outside the presentation layer, keep persistence concerns outside domain rules, and make dependencies explicit enough that the codebase remains understandable without external explanation.

The implementation philosophy is straightforward:

- Build the foundation before features.
- Keep behavior explicit and testable.
- Prefer small, focused components over broad abstractions.
- Treat documentation, tests, security, and operational readiness as part of implementation.
- Avoid introducing complexity that is not required by the product or architecture.

This blueprint is the primary engineering playbook for future implementation tasks. New features, refactors, tests, and documentation updates should be checked against this document before work begins.

## 2. Engineering Principles

Blogify API follows engineering principles that support maintainability, correctness, and long-term clarity.

**SOLID** principles should guide component design. Classes and modules should have focused responsibilities, depend on stable abstractions where appropriate, and remain easy to extend without modifying unrelated behavior. SOLID is not a reason to over-engineer; it is a tool for keeping responsibilities clear.

**DRY** should be applied to meaningful duplication, not superficial similarity. Shared behavior should be extracted when repetition creates maintenance risk, inconsistent behavior, or unclear ownership. Duplication may remain temporarily when abstraction would make intent harder to understand.

**KISS** requires the simplest design that satisfies the approved requirements. Implementation should avoid speculative patterns, unnecessary indirection, and premature generalization. A clear direct solution is preferred over a clever framework of abstractions.

**Explicit over implicit** means dependencies, validation rules, permission checks, and service boundaries should be visible in the code structure. Hidden framework behavior should not obscure business rules or security decisions.

**Composition over inheritance** should be the default design preference. Shared behavior should usually be assembled through small reusable components, services, helpers, policies, or mixins with narrow responsibilities. Inheritance is acceptable for stable base components but should not become a deep hierarchy.

**Convention where appropriate** means the project should use predictable naming, directory structure, response shapes, error contracts, and testing patterns. Conventions reduce decision fatigue, but they must remain documented and intentional.

## 3. Repository Structure

The repository structure should make architectural boundaries visible before a contributor opens individual files.

```text
blogify-api/
|-- config/
|-- apps/
|   |-- authentication/
|   |-- users/
|   |-- posts/
|   |-- comments/
|   |-- likes/
|   |-- bookmarks/
|   |-- categories/
|   |-- tags/
|   |-- common/
|   |-- core/
|-- services/
|-- tests/
|-- docs/
|-- scripts/
|-- prompts/
|-- .github/
|-- .env.example
|-- README.md
```

`config/` contains project configuration, routing entry points, settings composition, and runtime integration wiring. It should not contain feature business logic.

`apps/` contains the domain-oriented Django applications. Each application owns a bounded area of product behavior and should expose its behavior through clear service, API, permission, and validation boundaries.

`services/` contains shared application-level orchestration that spans multiple apps when the behavior does not belong cleanly to a single app. This directory must not become a dumping ground for unrelated utilities.

`tests/` contains project-level tests, cross-app integration tests, API contract tests, test utilities, factories, and fixtures that are shared across applications.

`docs/` contains approved project documentation, architecture decisions, diagrams, and implementation guidance. Documentation must remain versioned with the code it describes.

`scripts/` contains local development, maintenance, automation, and operational helper scripts. Scripts must be documented, safe to rerun where possible, and aligned with the single-command local development goal.

`prompts/` contains planning and review prompts used to produce project documentation. These files are project artifacts, not runtime application code.

`.github/` contains CI/CD workflow definitions, pull request templates, issue templates, and repository automation configuration.

`.env.example` documents required environment variables without containing secrets.

`README.md` provides the entry point for contributors and should direct readers to the appropriate planning, setup, testing, and operating documents.

## 4. Django Project Layout

The Django project layout should reflect the approved modular monolith architecture.

`config` owns project-level configuration, installed app registration, environment-specific settings composition, URL routing entry points, WSGI/ASGI entry points, and framework integration. It may connect infrastructure pieces, but it must not contain feature workflows, validation rules, permissions, or business decisions.

`apps` is the primary home for product capabilities. Each app should contain only the behavior needed for its bounded responsibility. Cross-app coordination should happen through services, not through direct coupling between views, serializers, or persistence details.

`core` contains project-wide infrastructure primitives that are not specific to one feature area. Examples include exception handling contracts, request metadata support, shared middleware foundations, application constants, and base types. `core` should stay small and stable.

`common` contains reusable application components shared by multiple feature apps. Examples include reusable permissions, pagination classes, filtering helpers, serializer foundations, and API response helpers. `common` should contain generic project patterns, not business behavior for a specific feature.

`services` contains application service orchestration for workflows that coordinate multiple apps or infrastructure components. Services own transaction boundaries, business workflow sequencing, and cross-entity rules that would otherwise leak into views.

`tests` contains test suites organized by behavior and scope. App-level tests may live near apps where useful, but shared integration, API, permission, and contract tests should remain discoverable in the project-level test structure.

`scripts` supports local development and repeatable operations. Scripts should make common workflows easier without becoming hidden implementation dependencies.

`docs` is part of the engineering system. Implementation work is incomplete when the code changes but the relevant documentation remains outdated.

## 5. Django App Responsibilities

Each application must have a clear responsibility, explicit boundaries, and controlled dependencies.

### authentication

**Responsibilities:** Authentication owns login, registration support, token lifecycle, token refresh, logout semantics, credential-related workflows, and authentication-specific security behavior.

**Boundaries:** It does not own user profile data, post ownership behavior, authorization rules for domain resources, or moderation decisions.

**Dependencies:** It may depend on `users` for identity records and on `common` or `core` for shared security, exception, and response behavior. It must not depend on posts, comments, likes, bookmarks, categories, or tags.

### users

**Responsibilities:** Users owns account identity, profile-facing user data, account status, ownership identity, and user-level product behavior required by other apps.

**Boundaries:** It does not own authentication token mechanics, post content, comments, bookmarks, or engagement records.

**Dependencies:** It may depend on `common` and `core`. Other apps may reference users as owners or actors, but user behavior should not be implemented inside those apps.

### posts

**Responsibilities:** Posts owns blog post lifecycle, draft and publication state, author ownership, content metadata, visibility rules, post discovery eligibility, and post-level business policies.

**Boundaries:** It does not own comments, likes, bookmarks, or authentication. It may expose post eligibility rules that other apps consume.

**Dependencies:** It may depend on `users`, `categories`, `tags`, `common`, and `core`. It should not depend on comments, likes, or bookmarks for core post behavior.

### categories

**Responsibilities:** Categories owns category identity, naming, slug behavior, activation status, and category-level organization of posts.

**Boundaries:** It does not own post content or post publication workflows.

**Dependencies:** It may depend on `common` and `core`. Posts may depend on categories, but categories should not depend on posts for core category behavior.

### tags

**Responsibilities:** Tags owns tag identity, normalized naming, slug behavior, activation status, and flexible post labeling.

**Boundaries:** It does not own post publication, post content, or discovery ranking.

**Dependencies:** It may depend on `common` and `core`. Posts may depend on tags through explicit association behavior.

### comments

**Responsibilities:** Comments owns comment creation, threaded replies, comment visibility, moderation status, ownership checks, and comment lifecycle.

**Boundaries:** It does not own post publication state, user identity, or authentication. It must respect post visibility and comment eligibility rules defined by the post domain.

**Dependencies:** It may depend on `posts`, `users`, `common`, and `core`. It should access post eligibility through services or domain policies instead of duplicating post rules.

### likes

**Responsibilities:** Likes owns user-to-post like behavior, uniqueness rules, engagement eligibility, and like removal behavior.

**Boundaries:** It does not own post metrics as source-of-truth content, post visibility, or user identity.

**Dependencies:** It may depend on `posts`, `users`, `common`, and `core`. It should use post eligibility rules and must not duplicate publication logic.

### bookmarks

**Responsibilities:** Bookmarks owns private user-to-post save behavior, bookmark uniqueness, bookmark removal, and bookmark visibility.

**Boundaries:** It does not own post content, public popularity, or authentication.

**Dependencies:** It may depend on `posts`, `users`, `common`, and `core`. Bookmark visibility must remain scoped to the authenticated owner unless an approved admin workflow requires otherwise.

### common

**Responsibilities:** Common owns reusable application components shared by feature apps, including base serializers, permissions, pagination, filtering helpers, API response helpers, and reusable validation utilities.

**Boundaries:** It must not contain feature-specific business rules. If a helper starts requiring knowledge of posts, comments, or users, it likely belongs in that feature app or a service.

**Dependencies:** It may depend on `core` and framework primitives where appropriate. Feature apps may depend on `common`; `common` should not depend on feature apps.

### core

**Responsibilities:** Core owns project-wide primitives such as base exceptions, error codes, request metadata, audit abstractions, middleware foundations, constants, and cross-cutting contracts.

**Boundaries:** It must not contain feature workflows or domain-specific product behavior.

**Dependencies:** It should have minimal dependencies and should not import feature apps. It may be depended on by every app.

## 6. Base Components

Base components exist to standardize repeated implementation patterns without hiding business behavior.

**BaseModel** should provide common persistence fields and lifecycle conventions such as UUID identity, audit timestamps, soft-delete support where applicable, and consistent default ordering behavior. It exists to keep entity metadata consistent, not to centralize domain rules.

**BaseSerializer** should standardize serializer behavior such as response metadata, common field handling, validation error formatting, and shared representation conventions. It should not contain feature-specific validation that belongs to a service or domain policy.

**BaseViewSet** should enforce consistent API behavior across resources, including request metadata propagation, permission integration, response shaping, and pagination conventions. It should remain thin and must not become a home for business workflows.

**BasePermission** should provide reusable permission composition patterns and common ownership/admin checks. Feature-specific permission decisions should remain explicit and testable.

**BasePagination** should enforce default pagination behavior, maximum page sizes, pagination metadata, and API consistency across collection endpoints.

**BaseFilter** should standardize filtering conventions, allowed query parameters, validation behavior, and predictable error handling for invalid filters.

**BaseManager** should encapsulate common query scopes such as active records, visible records, ownership-scoped records, and soft-delete behavior. Managers should improve query clarity without becoming business service objects.

**BaseService** should provide a consistent pattern for application services, including validation flow, transaction handling, logging context, exception mapping, and dependency boundaries. It should support workflow consistency without creating a rigid framework that obscures intent.

Every base component must justify its existence through repeated, real usage. If a base class only anticipates future needs, it should not be created yet.

## 7. Service Layer Strategy

The service layer is responsible for application workflows and business orchestration. It keeps views thin, keeps serializers focused on input and output contracts, and prevents business rules from leaking into persistence models.

Services should own:

- Multi-step workflows.
- Cross-entity validation.
- Transaction boundaries.
- Coordination between apps.
- Calls to infrastructure adapters.
- Business decisions that do not belong to one persistence entity.
- Emission of audit, logging, cache invalidation, or background job side effects.

Service names should be action-oriented and domain-specific. Names should make the workflow obvious, such as post publication, comment creation, bookmark creation, or authentication token refresh. Generic names such as `Manager`, `Helper`, or `Processor` should be avoided unless the responsibility is precise.

Transaction boundaries should be declared at service entry points for workflows that modify state. A service should either complete the intended state change or fail without leaving partial writes. Nested services should avoid starting independent transactions unless the workflow explicitly requires a separate consistency boundary.

Dependency direction must follow the approved architecture. API views call services. Services may call domain policies, repositories or managers, infrastructure adapters, and other application services when necessary. Services must not depend on presentation-layer classes or HTTP-specific behavior.

Validation flow should be layered:

1. Request shape and primitive type validation happen at the API contract boundary.
2. Business validation happens in services and domain policies.
3. Data integrity validation is enforced by database constraints and model-level persistence rules.
4. Cross-entity validation happens in services that can coordinate the relevant dependencies.

Business logic ownership should remain explicit. If a rule determines whether a user may publish a post, comment on a post, like a post, or view a draft, that rule belongs in a service, policy, or domain component, not in a view method or serializer representation.

## 8. Validation Strategy

Validation exists at multiple levels because each level protects a different boundary.

Serializer validation should verify request structure, required fields, basic value types, allowed enum values, field lengths, and API-facing input constraints. Serializer validation should not make complex business decisions that require coordinating multiple entities or infrastructure dependencies.

Business validation should enforce product rules, ownership rules, lifecycle rules, visibility rules, and cross-entity constraints. Examples include whether a post may be published, whether a comment may be added to a post, whether a user may bookmark a post, or whether a category is active.

Database validation should protect invariants that must remain true regardless of application path. Uniqueness, required relationships, referential integrity, and data consistency constraints should be enforced at the database level whenever possible.

Cross-entity validation should live in services or domain policies. This prevents validation logic from being duplicated across views, serializers, managers, and tasks.

Validation failures must produce predictable API errors using the approved error envelope. Error messages should be actionable for clients without exposing sensitive implementation details.

## 9. Permission Strategy

Permissions must be secure by default and consistent across the API.

Global permissions should deny unsafe actions unless the request is authenticated and explicitly allowed. Public read access is permitted only for resources approved as publicly visible, such as published posts and active categories or tags.

Object permissions should verify ownership, visibility, moderation state, and role-based access before returning or modifying a resource. Object-level checks are required for user-owned resources such as drafts, profiles, comments, likes, and bookmarks.

Role permissions should remain simple and explicit. The baseline roles are anonymous user, authenticated user, owner, admin, and system process. Additional roles should not be introduced unless approved by future requirements.

Ownership rules must be reusable and testable. A user should only modify their own drafts, comments, likes, bookmarks, and profile data unless an admin workflow explicitly permits broader access.

Admin behavior must be powerful but auditable. Admin actions should not bypass business rules silently. When an admin performs moderation, publication override, deactivation, or recovery behavior, the action should be logged or audited according to the approved logging and audit strategy.

Permissions should be implemented as reusable components where patterns repeat, but final permission decisions should remain readable at the API boundary.

## 10. Exception Handling Strategy

Exception handling must produce predictable client responses, useful logs, and clean separation between internal failures and public error contracts.

Custom exceptions should represent domain and application failures such as invalid state transitions, ownership violations, unavailable resources, duplicate actions, and business rule violations. These exceptions should carry stable error codes that map to the API error contract.

A global exception handler should convert framework, validation, authentication, permission, domain, and infrastructure exceptions into the approved response envelope. The handler should preserve request identifiers and avoid leaking stack traces, internal class names, database details, or sensitive values to clients.

Error mapping should be stable. A business conflict should map consistently to conflict semantics, validation failures should map consistently to validation semantics, and authentication or authorization failures should remain distinct.

Logging should capture unexpected exceptions with request metadata, actor identity where available, error code, affected resource, and stack trace. Expected business exceptions may be logged at lower severity or omitted from error logs when they represent normal client mistakes.

Client responses should be concise, deterministic, and safe. They should include a stable error code, human-readable message, optional field-level details, and request metadata.

## 11. Middleware Strategy

Middleware should handle request-level cross-cutting concerns only. It must not contain feature business logic.

Request ID middleware should assign or propagate a request identifier for every request. This identifier must appear in logs and API response metadata.

Logging middleware should record request start and completion events, duration, status code, request path, method, actor identity where available, and request identifier. It should avoid logging sensitive payloads.

Security middleware should enforce approved security headers, trusted proxy behavior, HTTPS assumptions, and safe request handling. Security behavior must be consistent across environments, with development-only relaxations documented explicitly.

Performance timing middleware should capture request duration and make slow requests observable. This supports performance review without requiring ad hoc instrumentation for every endpoint.

Future middleware may support correlation IDs, localization, API version metadata, or tenant-aware behavior if future requirements justify them. New middleware must be reviewed carefully because middleware affects every request.

## 12. Logging Strategy

Logging should make the system understandable in development, test, and production-like environments.

Application logs should describe meaningful lifecycle events such as authentication attempts, post publication, moderation actions, background job outcomes, cache failures, and unexpected workflow errors.

Security logs should capture authentication failures, suspicious access patterns, permission denials, token misuse signals, rate-limit events, and admin actions. Security logs must avoid storing credentials, tokens, or sensitive personal data.

Audit logs should record important state-changing actions where accountability matters, especially admin moderation, account status changes, publication changes, and destructive operations.

Error logs should capture unexpected failures with enough context to diagnose the issue. They should include request ID, correlation ID where available, actor identity where safe, component name, and stable error classification.

Structured logging is preferred over free-form text for operational events. Logs should be machine-searchable, consistent, and correlated across API requests, service workflows, and background jobs.

## 13. Caching Strategy

Redis may be used for caching, rate limiting support, background job coordination, and future performance-sensitive workflows. PostgreSQL remains the source of truth.

Caching should be introduced only where it solves a measured or clearly anticipated performance problem. Early implementation may define cache boundaries and invalidation strategy without caching every resource immediately.

Cache invalidation must be explicit. State-changing services that affect cached data should own or trigger invalidation. Cached public content must not continue exposing deleted, unpublished, private, or deactivated resources after state changes.

Cache keys should be predictable, versioned where useful, and scoped by resource, query, and user visibility where applicable. User-specific cache entries must never be shared across users.

Cache failures should degrade safely. The API should prefer recomputing from the database over failing a request solely because Redis is unavailable, except where Redis is required for a specific operational control such as rate limiting.

## 14. Background Processing

Celery is the approved background processing mechanism for asynchronous and scheduled work.

Email workflows should run asynchronously when they are not required to complete the original API request. This includes verification emails, notification emails, and future digest workflows.

Notifications should be queued when delivery does not need to block the client response. Notification tasks must be idempotent enough to tolerate retries.

Scheduled jobs may support maintenance workflows such as metric aggregation, cleanup of expired tokens, stale draft analysis, search index refreshes, or future operational checks.

Long-running tasks should not execute inside request-response cycles. The API should acknowledge accepted work and expose predictable state when clients need to observe completion.

Retry behavior must be intentional. Tasks should retry transient failures such as temporary external service errors. Tasks should not retry permanent business validation failures. Retry policies should include limits, backoff, and logging.

Background tasks must preserve data integrity. A task should verify current state before applying changes because the original triggering state may have changed after the task was queued.

## 15. Testing Strategy

Testing is a first-class deliverable. The project target is above 90% meaningful test coverage, but coverage percentage must not replace behavioral confidence.

Unit tests should verify small components such as validators, policies, service decisions, permissions, filters, and utility functions. They should be fast, focused, and easy to understand.

Integration tests should verify workflows that cross application, service, database, cache, and background job boundaries. They should prove that components cooperate correctly under realistic conditions.

API tests should verify request contracts, response envelopes, status codes, headers, authentication behavior, pagination metadata, filtering behavior, and error contracts.

Permission tests should cover anonymous, authenticated, owner, non-owner, admin, and system behavior for every protected resource. Permission regressions are considered high severity.

Performance tests should cover endpoints or workflows with meaningful scaling risk, including post listing, search, filtering, comments, popular content, and engagement-heavy workflows.

Factories should generate realistic test data while remaining explicit about important state. Factories should not hide the conditions that matter to a test.

Fixtures should be used sparingly for shared stable setup. Tests should prefer clear local setup when it improves readability.

Test suites should run in CI on every pull request. No feature is complete while tests are missing, flaky, skipped without justification, or disconnected from the acceptance criteria.

## 16. Code Organization Rules

Functions should remain small enough to understand without scrolling through unrelated responsibilities. As a practical guideline, functions that grow beyond roughly 40 lines should be reviewed for extraction, unless the logic is still linear and clearer in one place.

Class names, service names, test names, and module names should describe behavior, not implementation mechanics. Names such as `PostPublicationService`, `CanEditPostPermission`, or `PublishedPostFilter` are preferable to vague names such as `PostHelper`.

Imports should follow a consistent order: standard library, third-party packages, project modules, and local modules. Circular imports must be resolved by improving boundaries, not by hiding imports inside functions without a clear reason.

Comments should explain why a decision exists when the code alone cannot make the reason obvious. Comments should not restate simple behavior.

Documentation should be updated with any change that affects API behavior, architecture, setup, operations, security expectations, or contributor workflow.

Dependency direction must follow the approved architecture. Presentation depends on application services. Application services depend on domain policies and infrastructure abstractions. Domain rules do not depend on presentation concerns. Infrastructure does not define business behavior.

Shared utilities must be reviewed carefully. A shared module should have a stable, narrow purpose and should not become a place for unrelated code that lacks a clear owner.

## 17. Feature Development Order

Implementation should proceed in an order that reduces architectural risk and creates reusable foundations before feature volume increases.

### 1. Foundation

Establish project configuration, environment handling, repository structure, base components, exception handling, response envelopes, request IDs, logging foundations, local development workflow, CI, formatting, linting, and test infrastructure.

### 2. Authentication

Implement registration, login, token refresh, logout semantics, authentication errors, token security behavior, and authentication tests.

### 3. Users

Implement user identity behavior, profile behavior, account status handling, ownership foundations, and user-facing permission tests.

### 4. Categories

Implement category lifecycle, normalized naming, slug behavior, visibility, administrative management, and category filtering support.

### 5. Tags

Implement tag lifecycle, normalized naming, slug behavior, activation, and reusable tag association support.

### 6. Posts

Implement post draft and publication lifecycle, author ownership, category and tag association, visibility rules, publication rules, and post listing behavior.

### 7. Comments

Implement comment creation, threaded replies, ownership, moderation status, visibility behavior, and comment lifecycle rules.

### 8. Likes

Implement like creation, removal, uniqueness, post eligibility checks, and engagement metric update behavior.

### 9. Bookmarks

Implement private bookmark creation, removal, uniqueness, owner-only visibility, and bookmark listing behavior.

### 10. Search and Discovery

Implement search, filtering, sorting, pagination refinement, popular content, trending content, and performance-sensitive query review.

### 11. Documentation

Complete OpenAPI documentation, endpoint examples, setup documentation, deployment documentation, ADR references, and contributor workflow documentation.

### 12. Deployment

Finalize Dockerized local development, environment configuration, CI/CD validation, health checks, operational logging, release readiness, and deployment documentation.

Each phase should leave the system in a working state. Foundational shortcuts taken early will become expensive when feature apps begin depending on them.

## 18. Git Workflow

Development should happen on short-lived feature branches. Branch names should describe the work clearly and may use prefixes such as `feature/`, `fix/`, `docs/`, or `chore/`.

Commit messages should be concise, imperative, and scoped when useful. A conventional format such as `type(scope): summary` is preferred because it supports readable history and future automation.

Pull requests should include a clear summary, linked requirement or task context, test evidence, documentation updates, migration notes when applicable, and any security or performance considerations.

Review should focus on correctness, maintainability, security, architecture compliance, API contract stability, test coverage, and documentation completeness. Style-only feedback should be automated through formatting and linting where possible.

No feature should be merged while CI is failing, tests are missing, documentation is stale, or review comments remain unresolved.

## 19. Definition of Done

A feature is complete only when all of the following are true:

- Implementation is finished and aligned with approved architecture.
- Unit, integration, API, and permission tests are written where applicable.
- All relevant tests pass locally or in CI.
- Formatting passes.
- Linting passes.
- Type or static checks pass where configured.
- Documentation is updated.
- OpenAPI documentation is regenerated or updated.
- Error responses follow the approved contract.
- Security implications have been reviewed.
- Performance implications have been reviewed.
- Logging and audit behavior are implemented where required.
- Code review is complete.
- No unresolved review comments remain.
- The feature can be understood by a future maintainer without external explanation.

Definition of Done exists to prevent partially complete work from becoming technical debt. A feature that works locally but lacks tests, documentation, API contract updates, or security review is not production-ready.

## 20. Implementation Readiness Checklist

Before implementation begins, verify the following:

- Project vision is approved.
- Product requirements are approved.
- System architecture is approved.
- Database design is approved.
- API design is approved.
- Repository structure is finalized.
- Django project layout is defined.
- App boundaries are documented.
- Base component standards are defined.
- Service layer strategy is documented.
- Validation strategy is documented.
- Permission strategy is documented.
- Exception handling strategy is documented.
- Middleware strategy is documented.
- Logging strategy is documented.
- Caching strategy is documented.
- Background processing strategy is documented.
- Testing strategy is documented.
- Code organization rules are documented.
- Feature development order is documented.
- Git workflow is documented.
- Definition of Done is documented.
- ADRs exist or are planned for major architectural decisions.
- The engineering team can begin implementation without making additional architectural assumptions.

When this checklist is complete, Blogify API is ready to move from planning into implementation.
