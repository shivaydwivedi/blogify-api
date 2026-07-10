---
ADR: ADR-003
Title: Use a Service Layer for Business Workflows
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/02_System_Architecture.md
  - docs/04_API_Design.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Blogify API includes workflows that coordinate authentication, ownership, visibility, publication state, comments, engagement, caching, and background work.

Placing this behavior directly in views, serializers, or persistence models would make the system harder to test and would violate the approved layered architecture.

---

# Decision

Use a service layer for application workflows and business orchestration.

Business logic belongs in services, domain policies, and clearly named application components. It must not be implemented inside views, serializers, or persistence models.

Views should translate HTTP requests into service calls. Serializers should validate API shape and represent API data. Models should represent persistence state and durable constraints.

---

# Alternatives Considered

## Fat Views

Pros

- Simple for very small endpoints.
- Minimal ceremony at the beginning.

Cons

- Couples HTTP behavior to business rules.
- Harder to test business logic without API requests.
- Encourages duplication across endpoints.

---

## Fat Models

Pros

- Keeps some behavior close to data.
- Familiar pattern in many Django codebases.

Cons

- Can mix persistence concerns with workflow orchestration.
- Becomes awkward for cross-entity workflows.
- Makes infrastructure and side effects harder to isolate.

---

## Service Layer (Chosen)

Pros

- Keeps views thin.
- Makes business workflows testable.
- Provides clear transaction boundaries.
- Supports cross-app orchestration without circular dependencies.

Cons

- Adds an additional implementation layer.
- Requires naming discipline and review standards.

---

# Consequences

## Positive

- Business behavior is easier to locate and test.
- API contracts remain separate from business workflows.
- Future background jobs can reuse application behavior safely.

## Negative

- Poorly designed services can become procedural dumping grounds.
- Small features may require slightly more structure than a minimal implementation.

---

# Future Considerations

Services should remain action-oriented and focused. If service complexity grows, domain policies or smaller workflow components should be introduced instead of creating large generic service classes.

---

# References

- docs/02_System_Architecture.md
- docs/04_API_Design.md
- docs/05_Implementation_Blueprint.md
