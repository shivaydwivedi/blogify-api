# TASK 02 — System Architecture

You are the Lead Software Architect responsible for designing the complete software architecture for Blogify API.

Before producing any documentation, review and respect the following documents:

- MASTER_CONTEXT.md
- PROJECT_CONTEXT.md
- PHASE_00_CONTEXT.md
- docs/00_Project_Vision.md (Approved)
- docs/01_PRD.md (Approved)

Treat these documents as the source of truth.

Do not contradict previously approved decisions.

---

# Objective

Produce the complete System Architecture document for Blogify API.

The document should describe **how the software is organized**, not how it is implemented.

Avoid implementation details such as Django code, serializers, models, or database fields.

Instead, focus on architectural decisions, component responsibilities, communication patterns, scalability, and maintainability.

---

# Deliverables

Generate the complete contents of:

docs/02_System_Architecture.md

Additionally generate Mermaid diagrams where appropriate.

---

# The document must contain

## 1. Executive Overview

## 2. Architectural Goals

## 3. Architecture Style

Explain why Layered Architecture + Clean Architecture principles were selected.

Discuss advantages and trade-offs.

---

## 4. High-Level Component Diagram

Generate a Mermaid diagram showing:

Client

↓

API Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

↓

Database

Redis

Celery

External Services

---

## 5. Layer Responsibilities

Presentation Layer

Application Layer

Domain Layer

Infrastructure Layer

Explain what belongs in each layer.

Explain what should never belong there.

---

## 6. Django App Boundaries

Describe the responsibility of every app.

authentication

users

posts

comments

categories

tags

likes

bookmarks

common

core

config

---

## 7. Request Lifecycle

Generate a Mermaid sequence diagram illustrating a request from the client through middleware, authentication, services, database, and response.

---

## 8. Authentication Flow

Generate a Mermaid sequence diagram for JWT authentication.

---

## 9. Dependency Rules

Clearly define which layers are allowed to depend on which.

Prevent circular dependencies.

Explain dependency direction.

---

## 10. Cross-Cutting Concerns

Logging

Configuration

Exception Handling

Permissions

Validation

Caching

Pagination

Documentation

Testing

Monitoring

---

## 11. Scalability Considerations

Discuss:

Horizontal scaling

Redis

Background jobs

Stateless APIs

Database optimization

Future extensibility

---

## 12. Design Principles

Explain:

SOLID

DRY

KISS

Composition over inheritance

Explicit dependencies

Thin views

Service Layer

Reusable permissions

Environment-based configuration

---

## 13. Architecture Decision Summary

Summarize the most important architectural decisions.

---

## Writing Style

Professional engineering documentation.

Avoid unnecessary marketing language.

Avoid framework-specific tutorials.

Write documentation that could realistically be reviewed during an architecture review meeting.

---

# Constraints

Do NOT generate code.

Do NOT generate database tables.

Do NOT generate API endpoints.

Do NOT describe implementation details.

Remain architecture-focused.

---

# Final Goal

The document should be detailed enough that a senior backend engineer could begin implementing the system without needing further architectural clarification.