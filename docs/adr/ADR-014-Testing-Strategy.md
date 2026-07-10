---
ADR: ADR-014
Title: Adopt a Layered Testing Strategy
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/00_Project_Vision.md
  - docs/01_PRD.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Blogify API must demonstrate production-quality engineering. The project includes authentication, permissions, publication workflows, comments, engagement, search, caching, and background work that require confidence beyond manual testing.

---

# Decision

Use a layered testing strategy with unit tests, integration tests, API contract tests, permission tests, and performance-focused tests where appropriate.

The project target is above 90% meaningful coverage, supported by CI validation.

---

# Alternatives Considered

## Manual Testing Primarily

Pros

- Low initial setup.

Cons

- Not reliable for regressions.
- Weak evidence for production readiness.
- Does not support fast refactoring.

---

## API Tests Only

Pros

- Tests behavior from the client perspective.

Cons

- Slower feedback.
- Harder to isolate domain and service failures.
- May miss important internal edge cases.

---

## Layered Testing Strategy (Chosen)

Pros

- Provides fast feedback and broad behavioral confidence.
- Protects security and permission boundaries.
- Supports refactoring and future feature growth.

Cons

- Requires disciplined test organization.
- More initial setup than minimal testing.

---

# Consequences

## Positive

- Regressions are easier to catch.
- Business rules are documented through tests.
- CI can validate implementation readiness.

## Negative

- Test maintenance becomes part of feature work.
- Poorly designed tests can slow development if not reviewed.

---

# Future Considerations

Future work may add contract testing, load testing, mutation testing, or dedicated security test suites if the project scope expands.

---

# References

- docs/00_Project_Vision.md
- docs/01_PRD.md
- docs/05_Implementation_Blueprint.md
