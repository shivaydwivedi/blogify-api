# TASK 10 — Response Framework

You are a Senior Django REST Framework Engineer responsible for implementing the reusable response framework for Blogify API.

Before implementation review:

- Core Framework Blueprint
- API Design
- Exception Framework
- Base API Framework
- Coding Standards
- ADRs

These documents are mandatory.

---

## Goal

Implement a reusable response framework.

Every future API endpoint must return responses using this framework.

No business endpoints should be implemented.

---

## Implement

Create:

apps/common/responses/

Implement:

- APIResponse helper
- Success responses
- Created responses
- Updated responses
- Deleted responses
- Paginated responses
- Empty responses
- Error response helpers (compatible with the exception framework)

The implementation should align with the approved API Design document and integrate cleanly with the existing exception framework.

---

## Requirements

Framework only.

Do NOT implement:

- Authentication
- Feature endpoints
- Models
- Business serializers
- Business permissions
- URLs

---

## Verification

Verify:

✓ Django checks

✓ Imports

✓ Unit tests

✓ Response helper tests

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
- Suggested Commit Message
- Rollback Plan