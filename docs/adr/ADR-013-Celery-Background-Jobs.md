---
ADR: ADR-013
Title: Use Celery for Background Jobs
Status: Accepted
Date: 2026-07-10
Authors: Shivay Dwivedi
Related Documents:
  - docs/02_System_Architecture.md
  - docs/05_Implementation_Blueprint.md
---

# Context

Some workflows should not block API responses. Examples include email delivery, notifications, scheduled maintenance, metric aggregation, cleanup jobs, and future long-running work.

---

# Decision

Use Celery for asynchronous background jobs and scheduled tasks.

Background jobs should be idempotent where possible, retry transient failures safely, and verify current state before applying changes.

---

# Alternatives Considered

## Synchronous Request Processing

Pros

- Simple to reason about.
- No worker infrastructure.

Cons

- Slower API responses.
- Poor fit for retries and scheduled work.
- Couples external service delays to client requests.

---

## Custom Worker Implementation

Pros

- Full control.

Cons

- Unnecessary engineering effort.
- Higher risk than a proven task queue.

---

## Celery (Chosen)

Pros

- Mature background job framework.
- Supports retries and scheduled tasks.
- Works well with Redis and Django-style projects.

Cons

- Adds worker process and broker operations.
- Requires task idempotency and monitoring discipline.

---

# Consequences

## Positive

- API responses stay responsive.
- Long-running and retryable workflows are isolated.
- Scheduled jobs have a clear home.

## Negative

- Workers must be deployed and monitored.
- Background failures need logging and retry policies.

---

# Future Considerations

Future implementation may add dead-letter handling, task dashboards, priority queues, or separate worker pools if workload volume justifies them.

---

# References

- docs/02_System_Architecture.md
- docs/05_Implementation_Blueprint.md
