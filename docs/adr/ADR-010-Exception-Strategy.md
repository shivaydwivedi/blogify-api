---
ADR: ADR-010
Title: Centralize Exception Mapping
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/02_System_Architecture.md
  - docs/04_API_Design.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Application services, domain policies, infrastructure adapters, and API boundaries can all raise failures. These failures need consistent translation into API responses and logs.

---

# Decision

Use centralized exception mapping through a global exception handling strategy.

Domain and application exceptions should represent business failures. Framework and infrastructure exceptions should be translated into the approved API error contract at the boundary.

---

# Alternatives Considered

## Local Try-Catch Blocks Everywhere

Pros

- Gives each endpoint direct control.

Cons

- Creates inconsistent behavior.
- Duplicates mapping logic.
- Makes errors harder to audit and test.

---

## Framework Defaults Only

Pros

- Low implementation effort.

Cons

- Does not express business error semantics clearly.
- Produces inconsistent client-facing behavior.

---

## Centralized Exception Mapping (Chosen)

Pros

- Keeps error behavior consistent.
- Separates business failures from HTTP formatting.
- Improves observability and testability.

Cons

- Requires a maintained exception taxonomy.
- Incorrect mappings can affect many endpoints.

---

# Consequences

## Positive

- Error handling becomes predictable.
- Services can raise meaningful domain failures.
- API responses remain stable across endpoints.

## Negative

- New exception types require clear ownership.
- Global behavior must be covered by tests.

---

# Future Considerations

As the system grows, exception taxonomy may be refined by domain area while preserving a single mapping point for API responses.

---

# References

- docs/02_System_Architecture.md
- docs/04_API_Design.md
- docs/05_Implementation_Blueprint.md
