---
ADR: ADR-009
Title: Use a Stable API Error Contract
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/04_API_Design.md
  - docs/05_Implementation_Blueprint.md
---

# Context

API clients need predictable error responses for validation failures, authentication failures, permission denials, conflicts, rate limits, and unexpected errors.

Without a stable error contract, client behavior becomes fragile and error handling varies between endpoints.

---

# Decision

Use a consistent API error envelope with stable error codes, safe human-readable messages, optional details, and request metadata.

Error responses must not expose internal stack traces, database details, secrets, tokens, or implementation-specific class names.

---

# Alternatives Considered

## Framework Default Errors

Pros

- Minimal implementation effort.
- Useful during early development.

Cons

- Inconsistent response shapes.
- Can expose implementation details.
- Harder for clients to handle reliably.

---

## Endpoint-Specific Error Shapes

Pros

- Allows each endpoint to customize errors.

Cons

- Creates inconsistent API behavior.
- Increases client complexity.
- Makes documentation harder to maintain.

---

## Stable Error Contract (Chosen)

Pros

- Predictable for clients.
- Easier to document and test.
- Supports stable error codes across releases.

Cons

- Requires centralized mapping and discipline.
- Some framework errors must be normalized.

---

# Consequences

## Positive

- Clients can handle errors consistently.
- API documentation remains clearer.
- Error behavior becomes testable as part of the contract.

## Negative

- Implementation must maintain error code stability.
- New error cases require deliberate classification.

---

# Future Considerations

Future API versions may add richer error metadata, but existing error codes should not change meaning within the same version.

---

# References

- docs/04_API_Design.md
- docs/05_Implementation_Blueprint.md
