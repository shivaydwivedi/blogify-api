# TASK 11 — Utility Framework

You are a Senior Backend Engineer responsible for implementing the reusable utility framework for Blogify API.

Before implementation review:

- Core Framework Blueprint
- API Design
- Coding Standards
- Existing Framework
- ADRs

---

## Goal

Implement reusable utility modules.

These utilities must be generic.

They must not depend on business features.

---

## Create

apps/common/utils/

Implement:

- constants.py
- enums.py
- validators.py
- slug.py
- text.py
- datetime.py
- helpers.py

Each module should have one clear responsibility.

---

## Requirements

No feature logic.

No models.

No serializers.

No views.

No authentication.

Utilities only.

---

## Verification

Verify:

✓ Django checks

✓ Imports

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