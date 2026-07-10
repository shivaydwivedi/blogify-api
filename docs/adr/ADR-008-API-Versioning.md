---
ADR: ADR-008
Title: Use URL-Based API Versioning
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/04_API_Design.md
  - docs/01_PRD.md
---

# Context

Blogify API needs stable client contracts and room for future evolution. API consumers should be able to identify the contract version they are using without inspecting headers or documentation.

---

# Decision

Use URL-based API versioning with a version prefix such as `/api/v1`.

Backward-compatible changes may be introduced within the same version. Breaking changes require a new major API version.

---

# Alternatives Considered

## Header-Based Versioning

Pros

- Keeps URLs stable.
- Allows content negotiation patterns.

Cons

- Less visible during manual testing.
- Easier for clients to omit accidentally.
- More difficult to document clearly for beginner and portfolio audiences.

---

## Query Parameter Versioning

Pros

- Easy to test manually.
- Simple to add to requests.

Cons

- Treats versioning like an optional filter.
- Can reduce clarity around contract identity.

---

## URL-Based Versioning (Chosen)

Pros

- Explicit and easy to understand.
- Clear in documentation, logs, and client code.
- Strong fit for REST API contract management.

Cons

- Version appears in every route.
- New major versions require routing duplication or careful migration planning.

---

# Consequences

## Positive

- API contracts are visible and predictable.
- Documentation can be organized by version.
- Breaking changes have a clear migration path.

## Negative

- Teams must maintain compatibility rules within a version.
- Multiple supported versions increase maintenance cost if introduced later.

---

# Future Considerations

Future major versions should be introduced only for meaningful contract changes. Deprecation windows and migration guides should be documented before removing older versions.

---

# References

- docs/04_API_Design.md
- docs/01_PRD.md
