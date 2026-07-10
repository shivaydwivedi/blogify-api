---
ADR: ADR-012
Title: Use Redis for Caching and Operational Support
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/02_System_Architecture.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Blogify API may need caching, rate-limit support, background job coordination, and future performance improvements for read-heavy workflows such as public post discovery.

PostgreSQL remains the source of truth, but not every read or operational workflow should depend only on direct database access.

---

# Decision

Use Redis as the approved caching and lightweight operational data store.

Redis may support caching, rate limiting, Celery broker or result workflows where appropriate, and future derived performance optimizations. Redis must not become the source of truth for durable product data.

---

# Alternatives Considered

## No Cache Layer

Pros

- Simpler infrastructure.
- Fewer failure modes.

Cons

- Limits performance options.
- Makes rate limiting and background coordination harder.

---

## In-Process Cache

Pros

- Simple and fast within one process.

Cons

- Not shared across instances.
- Poor fit for horizontal scaling.
- Lost on restart.

---

## Redis (Chosen)

Pros

- Shared across application instances.
- Strong fit for caching, rate limiting, and background job infrastructure.
- Common production-ready tool.

Cons

- Adds operational dependency.
- Requires explicit invalidation and fallback strategy.

---

# Consequences

## Positive

- Supports scalable read optimization.
- Enables consistent operational workflows across instances.
- Aligns with the approved architecture and implementation blueprint.

## Negative

- Redis outages must be handled safely.
- Cache invalidation rules must be owned by services.

---

# Future Considerations

Redis usage should expand only where it solves a real performance or operational need. Cache behavior should be measured and reviewed before broad adoption.

---

# References

- docs/02_System_Architecture.md
- docs/05_Implementation_Blueprint.md
