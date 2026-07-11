# TASK 07 — Base Models

You are a Senior Django Backend Engineer responsible for implementing the reusable model foundation for Blogify API.

Before implementation, review:

- Core Framework Blueprint
- Implementation Blueprint
- Coding Standards
- System Architecture
- Database Design
- ADRs

These documents are mandatory.

---

## Goal

Implement the reusable model framework.

Every future model in Blogify should inherit from these classes.

This milestone creates infrastructure only.

No business models.

---

## Implement

### UUIDModel

Responsibilities:

- UUID primary key

Nothing else.

---

### TimestampedModel

Responsibilities:

- created_at
- updated_at

---

### SoftDeleteModel

Responsibilities:

- deleted_at
- is_deleted
- helper methods

No business rules.

---

### AuditModel

Prepare for:

- created_by
- updated_by

Design for future authentication integration.

---

### BaseModel

Compose the reusable mixins.

Avoid duplication.

---

### Managers

Implement reusable managers:

- ActiveManager
- DeletedManager
- AllObjectsManager

---

## Requirements

Use abstract models.

Follow Django best practices.

Avoid premature optimization.

No feature-specific code.

No authentication.

No users.

No posts.

No comments.

No serializers.

No views.

---

## Verification

Verify:

✓ Django checks

✓ Migrations succeed

✓ Tests pass

✓ Black

✓ isort

✓ flake8

Add unit tests for the reusable model behavior.

---

## Pull Request

Provide:

- Summary
- Files Added
- Files Modified
- Verification
- Risks
- Future Work
- Commit Message
- Rollback Plan