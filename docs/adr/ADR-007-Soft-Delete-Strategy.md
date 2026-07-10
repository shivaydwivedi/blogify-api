---
ADR: ADR-007
Title: Use Soft Delete Where Data History Must Be Preserved
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/03_Database_Design.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Blogify API manages user-generated content, comments, media metadata, taxonomy, moderation records, and engagement data. Some records should disappear from normal product views without losing history, relationships, or auditability.

Physical deletion is still appropriate for some reversible user actions, but not for every lifecycle event.

---

# Decision

Use soft delete where preserving references, moderation history, audit trails, or content lifecycle integrity is important.

Soft-deleted records must be excluded from public discovery and normal user workflows unless an explicit administrative or recovery workflow allows access.

Physical deletion may be used for records where historical preservation is not required, such as simple engagement toggles, unless future audit requirements change that decision.

---

# Alternatives Considered

## Physical Delete Everywhere

Pros

- Simpler queries.
- Less stored data.

Cons

- Loses moderation and recovery context.
- Can break historical references.
- Makes audits and lifecycle review harder.

---

## Soft Delete Everywhere

Pros

- Preserves all historical state.
- Enables broad recovery options.

Cons

- Adds query complexity to every entity.
- Retains data that may not need preservation.
- Can conflict with privacy or retention requirements if used carelessly.

---

## Selective Soft Delete (Chosen)

Pros

- Preserves important history.
- Keeps simple actions simple.
- Aligns deletion behavior with product and audit needs.

Cons

- Requires clear entity-by-entity rules.
- Requires consistent visibility filters.

---

# Consequences

## Positive

- Important content history can be preserved.
- Moderation and recovery workflows remain possible.
- Accidental destructive operations are easier to recover from.

## Negative

- Queries must consistently exclude soft-deleted records.
- Unique constraints and indexes may need to account for active versus deleted records.

---

# Future Considerations

Future privacy or retention requirements may require hard-delete workflows, anonymization, retention windows, or archival policies.

---

# References

- docs/03_Database_Design.md
- docs/05_Implementation_Blueprint.md
