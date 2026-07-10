# TASK 01 — Project Bootstrap

You are a Senior Backend Engineer at Stripe responsible for implementing the first engineering milestone of Blogify API.

Before writing any code, carefully review and follow every approved engineering document.

## Mandatory References

Use these documents as the source of truth.

- MASTER_CONTEXT.md
- PROJECT_CONTEXT.md
- PHASE_00_CONTEXT.md
- docs/00_Project_Vision.md
- docs/01_PRD.md
- docs/02_System_Architecture.md
- docs/03_Database_Design.md
- docs/04_API_Design.md
- docs/05_Implementation_Blueprint.md
- docs/06_Development_Roadmap.md
- docs/07_Coding_Standards.md

Also respect all accepted ADRs.

Do not contradict any approved architectural decision.

---

# Objective

Implement ONLY the initial project bootstrap.

This milestone establishes the engineering foundation.

No business features should be implemented.

No authentication.

No models.

No serializers.

No views.

No API endpoints.

No business logic.

---

# Deliverables

Create a production-ready Django project structure.

Use:

Python 3.12+

Django 5+

Django REST Framework

The resulting repository should contain:

```
config/

settings/

base.py

development.py

production.py

testing.py

apps/

common/

core/

tests/

requirements/

scripts/

docs/

manage.py

README.md

.env.example

.gitignore

pyproject.toml

pytest.ini
```

---

# Configure

Create a proper Django settings package.

Split configuration into:

base

development

production

testing

Load environment variables correctly.

---

# Install and Configure

Django

Django REST Framework

python-dotenv

drf-spectacular

django-filter

psycopg

Pillow

pytest

pytest-django

Black

isort

flake8

pre-commit

---

# Configure

INSTALLED_APPS

REST_FRAMEWORK

TIME_ZONE

LANGUAGE_CODE

STATIC

MEDIA

DEFAULT_AUTO_FIELD

Environment loading

Logging skeleton

---

# Requirements

The project must start successfully.

No warnings.

No placeholder code.

No TODO comments.

No dead files.

Keep the implementation clean and production-oriented.

---

# Constraints

Do NOT implement:

Authentication

Database models

Docker

Redis

Celery

GitHub Actions

Swagger URLs

Health endpoint

Business logic

API endpoints

These belong to later milestones.

---

# Deliverables

Update only the files necessary for this milestone.

Avoid generating unrelated code.

---

# Output

Implement the project directly inside the existing Blogify API repository.

Do not create a second project.

Preserve the existing documentation.

---

# Before finishing

Verify:

✓ Project runs successfully

✓ Settings load correctly

✓ Imports work

✓ Folder structure matches architecture

✓ No architectural decisions violate the approved documents

Only after verifying everything should implementation be considered complete.