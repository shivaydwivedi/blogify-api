# TASK 09 — Exception Framework

You are a Senior Django Backend Engineer responsible for implementing the reusable exception framework for Blogify API.

Before implementation, review:

- Core Framework Blueprint
- API Design
- Implementation Blueprint
- Coding Standards
- ADRs
- Existing Base API Framework

These documents are mandatory.

---

## Goal

Implement a reusable exception framework that will be shared by every module in Blogify API.

No business exceptions.

No feature-specific logic.

Infrastructure only.

---

## Implement

Create:

apps/common/exceptions/

Implement:

- BaseAPIException
- ValidationException
- BusinessRuleException
- PermissionDeniedException
- ResourceNotFoundException
- ConflictException
- RateLimitException

Implement:

- Global DRF Exception Handler

Implement:

- Centralized Error Codes

Ensure compatibility with the existing API response contract.

Integrate with the existing logging framework.

---

## Requirements

No feature logic.

No authentication.

No API endpoints.

No business models.

No feature serializers.

No feature permissions.

Framework only.

---

## Verification

Verify:

✓ Django checks

✓ Exception handler imports

✓ Unit tests

✓ Black

✓ isort

✓ flake8

✓ pytest

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