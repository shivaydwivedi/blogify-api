---
ADR: ADR-005
Title: Use UUIDs for Public Entity Identifiers
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/03_Database_Design.md
  - docs/02_System_Architecture.md
  - docs/01_PRD.md
---

# Context

Blogify API exposes public and authenticated resources such as users, posts,
comments, categories, tags, media assets, likes, and bookmarks.

Identifiers will appear in URLs, API responses, logs, documentation examples,
client state, and potentially future integrations. The identifier strategy must
avoid leaking record counts, support stable external references, and remain
compatible with future distributed workflows.

---

# Decision

Public entities use UUIDs as primary identifiers.

UUIDs are used for externally addressable durable entities where clients need a
stable reference.

UUIDs are not an authorization mechanism. All access must still be controlled
through authentication, authorization, ownership checks, and visibility rules.

---

# Reasons

- Safer URLs because identifiers do not reveal simple creation order or record
  counts.
- Better support for future distributed systems or import workflows where
  identifiers may be generated outside a single database sequence.
- Better external references for clients, integrations, logs, and documentation.

---

# Alternatives Considered

## Auto Increment IDs

Pros

- Smaller indexes.
- Better locality for inserts.
- Easier manual inspection during local development.

Cons

- Predictable public identifiers.
- Exposes approximate record creation order and volume.
- Less flexible for future distributed identifier generation.

---

## UUIDs (Chosen)

Pros

- Harder to guess than sequential identifiers.
- Safer for public URLs and external references.
- Better fit for future distributed workflows.

Cons

- Larger indexes.
- Less compact than integer identifiers.
- Can reduce index locality depending on UUID generation strategy.

---

# Consequences

## Positive

- Public identifiers are less predictable.
- Client references remain stable and globally unique.
- Future data movement or distributed generation is easier to support.

## Negative

- Indexes are larger than with auto increment identifiers.
- Developers need tooling and conventions for working with UUIDs in local
  debugging.
- UUID unpredictability improves safety but does not replace authorization.

---

# Future Considerations

If insert locality becomes a measured issue, the project can evaluate ordered
UUID variants or internal surrogate identifiers while preserving UUIDs as the
public identifier contract.

---

# References

- docs/03_Database_Design.md
- docs/02_System_Architecture.md
- docs/01_PRD.md
