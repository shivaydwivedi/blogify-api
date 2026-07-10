---
ADR: ADR-002
Title: Use a Modular Monolith
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/00_Project_Vision.md
  - docs/02_System_Architecture.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Blogify API requires clear module boundaries, maintainable implementation, and production-oriented engineering practices without unnecessary distributed systems complexity.

The project is educational and architectural in nature. It should demonstrate strong backend design while remaining understandable, locally runnable, and practical for a single repository.

---

# Decision

Build Blogify API as a modular monolith.

The system will be deployed as one backend application while organizing product capabilities into clear application boundaries such as authentication, users, posts, comments, categories, tags, likes, and bookmarks.

Module boundaries must remain explicit so future extraction is possible if real product scale requires it.

---

# Alternatives Considered

## Microservices

Pros

- Independent deployment per service.
- Clear service ownership at large organizational scale.
- Independent scaling for high-volume components.

Cons

- Adds network, deployment, observability, testing, and data consistency complexity.
- Creates distributed failure modes that do not support the current project objectives.
- Slows local development and architectural learning.

---

## Single Unstructured Application

Pros

- Fast initial setup.
- Few files and low early overhead.

Cons

- Encourages unclear boundaries.
- Makes business logic harder to locate and test.
- Becomes difficult to maintain as features grow.

---

## Modular Monolith (Chosen)

Pros

- Preserves simple deployment.
- Supports strong internal boundaries.
- Keeps local development efficient.
- Allows future service extraction if justified.

Cons

- Requires discipline to prevent cross-module coupling.
- Scaling remains application-level until specific modules are extracted or optimized.

---

# Consequences

## Positive

- Lower operational complexity.
- Clearer contributor experience.
- Easier testing and local development.
- Strong fit for the approved layered architecture.

## Negative

- Teams must enforce boundaries through review and tests.
- Independent deployment of individual domains is not available initially.

---

# Future Considerations

If a module develops independent scaling, ownership, or availability requirements, it may be extracted later. Extraction should be based on measured need, not architectural fashion.

---

# References

- docs/00_Project_Vision.md
- docs/02_System_Architecture.md
- docs/05_Implementation_Blueprint.md
