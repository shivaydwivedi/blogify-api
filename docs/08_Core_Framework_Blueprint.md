# Blogify API - Core Framework Blueprint

## 1. Executive Overview

The Core Framework defines the reusable foundation that future Blogify API
feature modules will use. It establishes shared conventions for models, API
components, services, exceptions, responses, permissions, utilities, and tests.

The goal is not to build a large internal framework for its own sake. The goal
is to remove predictable duplication before feature work begins, while keeping
business behavior explicit and easy to review. Blogify API will include
multiple modules with similar concerns: UUID identifiers, timestamps,
soft-delete behavior, consistent API responses, pagination, permission checks,
service orchestration, validation failures, and test setup. These concerns
should be implemented once, documented clearly, and reused consistently.

Building this reusable infrastructure before feature modules protects the
architecture in three ways:

- It keeps feature modules focused on product behavior.
- It prevents every app from inventing its own response, exception, permission,
  pagination, and testing patterns.
- It gives reviewers a stable baseline for evaluating feature implementation.

This document is an engineering design blueprint. It does not define Django
models, serializers, views, or implementation code. Sprint 1.5 should implement
the components described here, then future feature work should inherit or
compose those components where appropriate.

The framework must remain small, explicit, and accountable. Every reusable
component must solve a real repeated problem. If a component does not improve
clarity, consistency, or safety, it should not be added.

## 2. Design Principles

### DRY

The framework should remove meaningful duplication in cross-cutting behavior:
timestamps, UUID identifiers, soft-delete conventions, response envelopes,
pagination metadata, error contracts, permission bases, reusable validation,
and test utilities.

DRY should not be applied mechanically. Similar-looking behavior should remain
separate when the underlying product rules differ. A weak abstraction is worse
than honest duplication because it hides intent and makes future features
harder to change.

### SOLID

Framework components should have narrow responsibilities and stable contracts.
A base model should not know about API responses. A serializer base should not
contain business workflow rules. A permission base should not decide product
lifecycle rules. A service base should not become a generic execution engine
that obscures feature behavior.

SOLID should help engineers locate responsibility quickly. It should not create
deep inheritance chains or pattern-heavy code.

### Convention over Configuration

The framework should provide sensible project conventions so feature modules do
not repeatedly configure common behavior. Examples include timestamp field
names, UUID public identifiers, default pagination metadata, error envelope
shape, and common test assertions.

Conventions must be documented and predictable. When a feature needs to depart
from a convention, the exception should be explicit and justified.

### Explicit over Implicit

Reusable components must not hide important behavior. Permission checks,
service calls, validation flow, transaction boundaries, and response shaping
should remain visible at the feature boundary.

Implicit behavior is especially risky for security, permissions, and data
visibility. The framework should reduce boilerplate without making it hard to
see why a request is allowed, why data is visible, or why a workflow succeeds.

### Composition over Inheritance

The framework should prefer composition for optional behavior. A feature should
be able to combine a UUID identity component, timestamp behavior, soft-delete
behavior, reusable permissions, and service helpers without being forced into
an inflexible hierarchy.

Inheritance is acceptable for stable base types that match Django or DRF
extension points, but inherited behavior must remain shallow and obvious.

### Clean Architecture Alignment

The framework must preserve the approved layered architecture:

- API components adapt HTTP requests and responses.
- Services coordinate application workflows.
- Domain policies express business rules.
- Infrastructure components support persistence, logging, caching, and
  background processing.

Framework components must not collapse these boundaries. The framework should
make the architecture easier to follow, not easier to bypass.

## 3. Base Models

Base model components define shared persistence conventions. They should be
abstract, composable, and limited to data lifecycle concerns. They must not
contain feature-specific business logic.

### BaseModel

BaseModel is the general foundation for persistent entities that need standard
project behavior. It may compose common identity, timestamp, lifecycle, and
audit behavior where appropriate.

Provides:

- A consistent foundation for project entities.
- Shared metadata conventions.
- A stable place for persistence-level behavior that applies broadly.
- Common ordering or representation conventions when they are universal.

Should not contain:

- Feature-specific validation.
- Business workflows.
- Permission checks.
- API response behavior.
- Cross-app orchestration.

BaseModel should remain small. If it grows because unrelated components need
different behavior, those behaviors should be split into narrower model bases.

### TimestampedModel

TimestampedModel provides creation and update timestamps for entities that need
lifecycle tracking.

Provides:

- `created_at` semantics.
- `updated_at` semantics.
- Consistent timezone-aware timestamp behavior.
- A common foundation for sorting, auditing, and operational review.

Should not contain:

- Publication timestamps.
- Deletion timestamps.
- Moderation timestamps.
- Business lifecycle state transitions.

Feature-specific timestamps such as `published_at`, `deleted_at`, or
`moderated_at` should be defined by the component that owns that lifecycle.

### UUIDModel

UUIDModel provides a public, non-sequential identifier strategy aligned with
ADR-005.

Provides:

- UUID-based public identity.
- Consistent identifier generation.
- Safer externally visible references than sequential IDs.
- A foundation for API URLs, logs, and future integrations.

Should not contain:

- Authorization behavior.
- Ownership behavior.
- Slug behavior.
- Assumptions that UUID secrecy is a security boundary.

UUIDs reduce predictability, but permissions and visibility rules must still
protect all resources.

### SoftDeleteModel

SoftDeleteModel provides a reusable lifecycle pattern for records that should
be hidden from normal workflows without being physically removed immediately.

Provides:

- Deletion state tracking.
- A deletion timestamp where appropriate.
- Query conventions for active versus deleted records.
- Support for moderation, recovery, and reference preservation.

Should not contain:

- Feature-specific deletion rules.
- Authorization checks for deletion.
- Public visibility rules beyond generic active/deleted filtering.
- Data retention or privacy policy decisions that belong to product or
  compliance requirements.

Soft delete must be applied selectively. Likes or bookmarks may not need soft
delete unless audit requirements justify it. Posts, comments, taxonomy, media,
and moderation-sensitive records are stronger candidates.

### AuditModel

AuditModel provides shared persistence metadata for accountability and
traceability.

Provides:

- Actor references where the actor is known.
- Creation and update attribution where applicable.
- A foundation for administrative review and operational debugging.
- Consistent audit metadata across sensitive state changes.

Should not contain:

- Full audit event storage for every workflow.
- Business approval rules.
- Logging implementation.
- Permission decisions.

AuditModel metadata is not a substitute for audit events. Sensitive workflows
may still need dedicated audit records when the product requires durable
event-level traceability.

## 4. Base API Components

Base API components define consistent presentation-layer behavior. They should
keep views thin, responses predictable, and API contract behavior aligned with
the approved API design.

### BaseAPIView

BaseAPIView provides shared behavior for API views that are not naturally
resource-oriented viewsets.

Responsibilities:

- Apply common request metadata handling.
- Support consistent exception translation.
- Provide access to shared response helpers.
- Preserve authentication and permission integration.
- Keep action-specific views aligned with project response conventions.

BaseAPIView should not contain business workflows, direct persistence
orchestration, or feature-specific authorization rules.

### BaseViewSet

BaseViewSet provides shared behavior for resource-oriented API components.

Responsibilities:

- Standardize action-level permission hooks.
- Integrate pagination and response formatting.
- Preserve thin request handling.
- Delegate workflows to services.
- Support consistent serializer selection where needed.

BaseViewSet should not become a broad controller abstraction. Feature viewsets
must remain readable and explicit about the services and permissions they use.

### BaseSerializer

BaseSerializer provides shared API input and output conventions.

Responsibilities:

- Standardize validation error formatting.
- Support common metadata representation.
- Protect server-controlled fields from client input.
- Align output field naming with snake_case conventions.
- Keep request-shape validation separate from business validation.

BaseSerializer should not contain cross-entity business decisions, permission
checks, database orchestration, or workflow side effects.

### BasePermission

BasePermission provides reusable authorization patterns.

Responsibilities:

- Support authenticated-only checks.
- Support owner checks.
- Support admin checks.
- Support owner-or-admin combinations.
- Support object-level permission composition.
- Return predictable permission failure behavior.

BasePermission should not duplicate domain lifecycle rules. For example, a
permission may ask whether the requester owns a post, but whether a post may be
published belongs in a service or domain policy.

### BasePagination

BasePagination provides consistent collection metadata and limits.

Responsibilities:

- Enforce default page size.
- Enforce maximum page size.
- Return consistent pagination metadata.
- Support predictable empty collection behavior.
- Align with the API design document's pagination contract.

BasePagination should not contain resource-specific sorting, filtering, or
visibility rules.

### BaseFilter

BaseFilter provides shared filtering conventions.

Responsibilities:

- Validate supported query parameters.
- Reject unknown or invalid filter values.
- Normalize common filter inputs.
- Support clear validation errors for unsupported filters.
- Keep filter behavior explicit and documented.

BaseFilter should not bypass permission or visibility rules. Query filtering
must work with service or domain-level visibility enforcement.

## 5. Service Layer Foundation

The service layer foundation defines reusable workflow conventions without
hiding feature behavior.

### BaseService

BaseService provides a common structure for application services.

Responsibilities:

- Define a predictable service execution pattern.
- Provide a standard place for validation flow.
- Support transaction boundary conventions.
- Normalize known service errors into project exceptions.
- Support structured logging context where appropriate.

BaseService should not become a large framework. Feature services must still
make their workflow steps readable. If the base service makes business logic
harder to follow, it is too abstract.

### Transaction Boundaries

Transactions should be owned by service entry points for workflows that mutate
state. A service should either complete the intended state change or fail
without leaving partial writes.

Transaction boundaries should be explicit for:

- Multi-step create or update workflows.
- Publication transitions.
- Deletion or soft-delete workflows.
- Engagement actions that update derived metrics.
- Workflows that enqueue background jobs after durable state changes.

Read-only services should not open transactions unless they require consistent
reads across multiple queries.

### Validation Flow

Validation should proceed in layers:

1. API components validate request shape and primitive values.
2. Services validate workflow eligibility and cross-entity rules.
3. Domain policies validate product invariants.
4. Database constraints protect durable integrity.

The service layer should not rely on API serializers as the only protection.
Background jobs, CLI operations, and future internal workflows may call
services without the API boundary.

### Error Propagation

Services should raise project-defined exceptions for expected failures:
validation failures, business rule violations, permission failures, missing
resources, and state conflicts.

Services should not return ambiguous failure values such as `None` or `False`
when the caller needs to distinguish why the workflow failed. Expected errors
should carry stable error codes that the API exception handler can translate
into the approved response contract.

Unexpected infrastructure failures should be logged and allowed to propagate to
the global exception handler unless the service has a specific recovery path.

## 6. Exception Framework

The exception framework defines predictable application failures and maps them
to the API error contract.

### BaseAPIException

BaseAPIException is the root for project-defined client-facing exceptions.

Responsibilities:

- Carry a stable machine-readable error code.
- Carry a safe human-readable message.
- Optionally carry structured details.
- Support consistent mapping to HTTP response semantics.
- Preserve internal logging context separately from client-facing content.

BaseAPIException should not expose stack traces, database errors, secret
values, raw tokens, or implementation class names to clients.

### ValidationException

ValidationException represents invalid input or invalid request semantics.

Use for:

- Invalid field values.
- Missing required input.
- Unsupported query parameters.
- Invalid filter or sorting values.
- Cross-field request inconsistency.

ValidationException should support field-level details where useful.

### BusinessException

BusinessException represents a valid request shape that violates product rules
or current resource state.

Use for:

- Publishing an incomplete post.
- Commenting on a post that cannot accept comments.
- Liking an unavailable post.
- Exceeding comment nesting rules.
- Attempting an invalid lifecycle transition.

BusinessException should make business failures explicit without tying them to
HTTP status codes inside domain logic.

### PermissionException

PermissionException represents an authenticated or anonymous requester lacking
access to perform an action.

Use for:

- Owner-only updates attempted by non-owners.
- Admin-only actions attempted by normal users.
- Private bookmark access attempted by another user.
- Unauthorized mutation attempts.

PermissionException should support not-found masking where resource existence
must not be revealed.

### NotFoundException

NotFoundException represents resources that do not exist or are not visible to
the requester.

Use for:

- Missing records.
- Soft-deleted records hidden from normal workflows.
- Drafts requested by non-owners.
- Private resources hidden from unauthorized users.

NotFoundException should avoid revealing whether the resource does not exist or
is hidden unless the requester has permission to know.

### Global Exception Handling Philosophy

The global exception handler should be the single presentation-layer boundary
that converts project, framework, validation, authentication, permission, and
unexpected errors into API responses.

Expected exceptions should return stable response envelopes. Unexpected
exceptions should be logged with request context and returned as safe generic
errors. The handler must preserve request identifiers when available.

## 7. Response Framework

Blogify API should use one consistent response format across resources.

### Success Response

Successful single-resource responses should include:

- `data`: the resource or action result.
- `meta`: request metadata such as request ID or correlation ID when available.

The response should not expose internal model details, private fields, or
server-controlled values not intended for clients.

### Error Response

Error responses should include:

- `error.code`: stable machine-readable code.
- `error.message`: safe human-readable message.
- `error.details`: optional structured detail.
- `meta`: request metadata.

Error codes should be stable within an API version. Error messages may improve
for clarity but must not expose sensitive data.

### Pagination Response

Paginated collection responses should include:

- `data`: list of resources.
- `pagination.page`: current page number where page pagination is used.
- `pagination.page_size`: requested or applied page size.
- `pagination.total_count`: total count when available.
- `pagination.total_pages`: total pages when available.
- `pagination.next`: next page indicator or URL where appropriate.
- `pagination.previous`: previous page indicator or URL where appropriate.
- `meta`: request metadata.

The default page size should be 20 and the maximum page size should be 100,
aligned with the API design document.

### Validation Response

Validation responses should use the standard error response and include
field-level details when possible.

Validation details should identify:

- Field name.
- Stable validation code where possible.
- Safe message.
- Rejected value only when safe to echo.

### Authentication Response

Authentication failures should use the standard error response. Messages must
avoid account enumeration. Token failures should distinguish client-actionable
states only where safe and documented, such as missing credentials, invalid
credentials, expired token, or insufficient authentication.

Authentication success responses are feature-specific and should be defined in
the authentication implementation while preserving the success envelope.

## 8. Permission Framework

The permission framework should provide reusable building blocks for common
authorization behavior.

### Reusable Permissions

Reusable permission components should cover:

- Public read access.
- Authenticated-only access.
- Owner-only access.
- Admin-only access.
- Owner-or-admin access.
- Safe-method access.
- Object visibility access.

Permissions should be small and composable. A feature should be able to combine
common permissions with feature-specific policies without duplicating logic.

### Ownership

Ownership checks should be explicit and testable. The framework should support
consistent ownership resolution for common ownership shapes, such as resources
owned directly by a user or resources owned through a parent object.

Ownership checks should never trust client-submitted owner identifiers.
Ownership must be derived from authenticated identity and server-side data.

### Role-Based Permissions

Role-based permissions should support the approved role hierarchy:

- Anonymous user.
- Authenticated user.
- Owner.
- Administrator.
- System or operator context where explicitly defined.

Additional roles should not be introduced without product and architecture
approval.

### Object-Level Permissions

Object-level permissions should protect detail, update, delete, moderation, and
private collection workflows.

The framework should make object-level checks hard to forget. Public list
queries must still apply visibility rules before objects are returned.

## 9. Utility Layer

The utility layer contains small reusable helpers that are broadly useful and
not owned by a specific feature module.

### Slug Generation

Slug utilities should normalize titles, category names, tag names, and other
human-readable identifiers into URL-safe values.

Slug helpers should not decide uniqueness rules alone. Uniqueness belongs to
the owning feature and database constraints.

### Read-Time Calculation

Read-time utilities should estimate reading duration from content length or
word count.

Read-time helpers should be deterministic and independent of persistence. They
should not own post publication or content validation rules.

### Markdown Helpers

Markdown helpers may support normalization, safe rendering decisions, or future
content processing.

Markdown utilities must not allow unsafe HTML or script behavior. Security
review is required before rendered markdown is exposed to clients.

### Validators

Reusable validators should cover common formats and limits:

- Slug format.
- Username-like values.
- Query parameter ranges.
- Page size limits.
- File extension or content-type checks when media is implemented.

Feature-specific validation should remain in feature modules or services.

### Constants

Constants should centralize stable, shared values such as default pagination
size, maximum pagination size, common cache TTLs, upload limits, and shared
error codes.

Constants should not become a dumping ground. Values used by only one feature
should remain in that feature until they become genuinely shared.

### Enums

Enums should represent stable sets of allowed values such as lifecycle states,
visibility states, moderation states, sort directions, or system event names.

Enums should be explicit, documented, and compatible with API and database
contracts.

### Date Utilities

Date utilities should support timezone-aware operations, ISO-8601 formatting,
date range validation, and safe comparison helpers.

Date utilities must preserve UTC conventions unless a feature explicitly
requires localized display behavior at the client boundary.

## 10. Testing Foundation

The testing foundation should make consistent, high-quality tests easier to
write across all modules.

### Base Test Classes

Base test classes may provide common setup for API tests, service tests,
permission tests, and integration tests.

They should not hide important test preconditions. A test reader should still
be able to understand the actor, resource state, permissions, and expected
outcome.

### Factories

Factories should create realistic test data with clear defaults.

Factory responsibilities:

- Reduce repetitive object setup.
- Make ownership explicit.
- Support published, draft, soft-deleted, active, inactive, and moderated
  states where applicable.
- Avoid hidden side effects unless the factory name makes them clear.

Factories should not replace scenario-specific setup when explicit setup makes
the test easier to understand.

### Fixtures

Fixtures should provide stable reusable test context:

- Anonymous API client.
- Authenticated API client.
- Admin API client.
- Common users.
- Common categories or tags when needed.
- Celery eager mode where background tasks are tested.

Fixtures should be scoped carefully to avoid hidden coupling between tests.

### Authenticated Clients

Authenticated test clients should make identity and role explicit.

The testing framework should support:

- Normal authenticated user.
- Resource owner.
- Non-owner.
- Admin user.
- Anonymous client.

Permission tests should use these clients systematically.

### Reusable Assertions

Reusable assertions should cover:

- Success response envelope.
- Error response envelope.
- Validation error details.
- Pagination metadata.
- Authentication failure.
- Permission denial.
- Not-found masking.
- Soft-delete visibility.
- Ownership enforcement.

Assertions should improve test readability without hiding the behavior being
verified.

## 11. Dependency Rules

Feature modules may depend on the Core Framework for reusable base models, API
components, exceptions, response helpers, permissions, utilities, and test
support.

The Core Framework must never depend on feature modules.

Allowed dependency direction:

- Feature apps depend on `apps.common` for reusable API, serializer,
  permission, pagination, filter, utility, and response components.
- Feature apps depend on `apps.core` for project-wide operational primitives,
  exception contracts, task infrastructure, and system-level concerns.
- Feature services may depend on shared service foundations.
- Project-level tests may depend on test utilities and factories.

Disallowed dependency direction:

- `apps.common` importing posts, comments, users, likes, bookmarks,
  categories, tags, or authentication.
- `apps.core` importing feature business modules.
- Shared utilities depending on feature models.
- Base API components calling feature services directly.
- Base permissions encoding feature-specific product rules.
- Base models knowing about post, comment, bookmark, or user workflows.

When a shared component starts needing feature knowledge, it should be moved
out of the framework and into the owning feature module. If multiple features
need similar behavior, the team should extract only the stable shared contract,
not the product-specific rule.

## 12. Extension Strategy

Future apps should extend the Core Framework deliberately.

Feature modules should:

- Use base model components only when the lifecycle behavior applies.
- Use BaseSerializer to preserve API contract consistency.
- Use BaseViewSet or BaseAPIView only when they reduce repeated boundary code.
- Use reusable permissions and add feature-specific policies where needed.
- Use BaseService for workflow conventions while keeping business steps
  explicit.
- Raise project exceptions for expected failures.
- Return responses through the shared response framework.
- Use shared test foundations for API, permission, service, and integration
  tests.

Extension should be opt-in and understandable. A feature should not inherit
from a base component merely because it exists. The question should always be:
does this component make the feature clearer, safer, or more consistent?

When future requirements introduce new reusable needs, the team should follow
this process:

1. Implement behavior locally in the owning feature when only one feature needs
   it.
2. Extract shared behavior only after repetition appears or a clear
   cross-feature contract exists.
3. Document the shared component's responsibility and boundaries.
4. Add tests that protect both the shared component and at least one real usage.
5. Update this blueprint or related engineering documentation if the framework
   contract changes.

This extension strategy keeps the framework useful without turning it into a
speculative platform.

## 13. Implementation Readiness Checklist

Before Sprint 1.5 implementation begins, verify that every reusable component
has a defined responsibility, boundary, and dependency direction.

- BaseModel responsibility is defined.
- TimestampedModel responsibility is defined.
- UUIDModel responsibility is defined.
- SoftDeleteModel responsibility is defined.
- AuditModel responsibility is defined.
- BaseAPIView responsibility is defined.
- BaseViewSet responsibility is defined.
- BaseSerializer responsibility is defined.
- BasePermission responsibility is defined.
- BasePagination responsibility is defined.
- BaseFilter responsibility is defined.
- BaseService responsibility is defined.
- Transaction boundary guidance is defined.
- Validation flow is defined.
- Error propagation guidance is defined.
- BaseAPIException responsibility is defined.
- ValidationException responsibility is defined.
- BusinessException responsibility is defined.
- PermissionException responsibility is defined.
- NotFoundException responsibility is defined.
- Global exception handling philosophy is defined.
- Success response format is defined.
- Error response format is defined.
- Pagination response format is defined.
- Validation response format is defined.
- Authentication response guidance is defined.
- Reusable permission categories are defined.
- Ownership permission guidance is defined.
- Role-based permission guidance is defined.
- Object-level permission guidance is defined.
- Utility layer categories are defined.
- Testing foundation categories are defined.
- Framework dependency rules are defined.
- Extension strategy is defined.
- The blueprint contains no implementation code.
- The blueprint does not define Django models, serializers, views, or endpoint
  implementations.

When this checklist is complete, Sprint 1.5 can implement the Core Framework
without making additional architectural assumptions.
