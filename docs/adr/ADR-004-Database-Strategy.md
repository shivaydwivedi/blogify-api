---
ADR: ADR-004
Title: Adopt PostgreSQL and a Normalized Relational Database Strategy
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/03_Database_Design.md
  - docs/02_System_Architecture.md
  - docs/01_PRD.md
---

# Context

Blogify API requires durable storage for users, profiles, posts, categories,
tags, nested comments, likes, bookmarks, media metadata, moderation records,
audit events, and derived discovery metrics.

The product has strong relational requirements: users own posts, posts belong
to categories, posts have many tags, posts receive comments and engagement,
bookmarks are private to users, and moderation must preserve traceable
relationships.

The database must support maintainability, integrity, clear ownership,
efficient public discovery queries, and future extensibility without adding
unnecessary distributed data complexity.

---

# Decision

Use PostgreSQL as the source of truth for durable product state.

Use a normalized relational model for core product entities and relationships.

Use UUID primary identifiers for publicly addressable durable entities.

Keep derived metrics separate from source records so engagement counts and
ranking signals remain rebuildable.

Use soft delete where preserving references, moderation history, auditability,
or content lifecycle integrity is important.

---

# Alternatives Considered

## Document Database

Pros

- Flexible document shape.
- Can be convenient for nested content structures.

Cons

- Weaker fit for relational ownership and uniqueness rules.
- More application-side enforcement for joins and constraints.
- Less aligned with the project's relational data modeling goals.

---

## Fully Denormalized Relational Model

Pros

- Can simplify some read paths.
- Can reduce joins for selected queries.

Cons

- Increases data duplication.
- Makes consistency harder to reason about.
- Weakens clarity for a portfolio project focused on clean data modeling.

---

## PostgreSQL with Normalized Relational Model (Chosen)

Pros

- Strong fit for ownership, taxonomy, engagement, and moderation relationships.
- Supports foreign keys, uniqueness constraints, indexing, and transactions.
- Keeps business concepts explicit and reviewable.
- Allows selective derived data where performance requires it.

Cons

- Requires disciplined query design for read-heavy workflows.
- Normalized reads can require joins.
- Derived metrics require update or rebuild strategy.

---

# Consequences

## Positive

- Strong data integrity for core business rules.
- Clear relationships between users, posts, comments, taxonomy, and engagement.
- Better support for transactional workflows and consistency boundaries.
- Reviewers can reason about the data model from established relational
  principles.

## Negative

- More careful index planning is required.
- Joins must be managed intentionally for public list and discovery workflows.
- Soft deletion requires consistent visibility filtering.
- Derived metrics introduce consistency and rebuild responsibilities.

---

# Future Considerations

If traffic grows, the system can add read replicas, targeted caching,
background aggregation, table partitioning for audit-style data, or specialized
search infrastructure without replacing PostgreSQL as the source of truth.

---

# References

- docs/03_Database_Design.md
- docs/02_System_Architecture.md
- docs/01_PRD.md
