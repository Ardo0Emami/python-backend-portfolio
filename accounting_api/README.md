# Accounting API

A small but production-oriented backend service implementing a basic accounting domain.
The project is intentionally scoped to remain simple, while demonstrating clear architectural boundaries,
correct transaction handling, and maintainable code structure.

The focus of this codebase is correctness, clarity, and long-term maintainability rather than feature count.

---

## Overview

The service models a minimal accounting system with the following core concepts:

- Customers
- Invoices
- Line items
- Derived invoice totals
- Explicit lifecycle states for invoices

The application is built using FastAPI and SQLAlchemy and follows a layered architecture
that separates HTTP concerns, business logic, persistence, and infrastructure.

---

## Architecture

The project follows a Clean Architecture–inspired structure with explicit boundaries between layers.

```text
app/
├── api/                      # HTTP layer (FastAPI routes, dependencies, middleware)
├── services/                 # Application use-cases and business rules
├── repositories/             # Persistence abstraction (SQLAlchemy-based)
├── models/
│   ├── sqlalchemy_models.py  # ORM entities
│   └── schemas/              # Pydantic request/response models
├── core/
│   ├── config.py             # Environment-based configuration
│   ├── db_infrastructure.py  # Engine and DB setup
│   └── db_adapter.py         # Session lifecycle and transaction boundaries
└── main.py                   # Application entry point
```

### Layer responsibilities

- **API layer**
  - Handles HTTP routing, request validation, and response formatting
  - Applies authentication and dependency injection
  - Does not contain business logic

- **Service layer**
  - Implements application use-cases
  - Enforces domain rules and invariants
  - Raises domain-specific errors

- **Repository layer**
  - Encapsulates all database access
  - Performs CRUD operations
  - Contains no business decisions

- **Infrastructure**
  - Database engine and session configuration
  - Environment-based settings
  - Cross-cutting concerns such as logging

---

## Domain Model

### Customer

- Represents a business customer
- Can own multiple invoices
- Automatically timestamped on creation

### Invoice

- Belongs to a single customer
- Has an explicit status lifecycle (draft, issued, paid)
- Aggregates line items
- Exposes a computed total amount derived from line items

### Line Item

- Belongs to a single invoice
- Represents a billable entry with quantity and unit price

Invoice totals are computed using a SQLAlchemy hybrid property, allowing both
in-Python access and efficient SQL-level aggregation.

---

## Database and Transactions

The application uses a **unit-of-work per request** model:

- One database session is created per HTTP request
- The session is committed only if the request completes successfully
- Any exception triggers a rollback
- Sessions are always closed deterministically

Repositories use `flush()` when identifiers are required, but do not manage commits.
Transaction boundaries are handled centrally at the API boundary.

This approach ensures atomicity and avoids scattered transaction logic.

---

## Authentication

Write operations are protected using a lightweight API key mechanism:

- API key is provided via request headers
- Validation occurs at the API boundary
- Business logic remains unaware of authentication concerns

This approach is suitable for internal or service-to-service APIs and avoids unnecessary complexity.

---

## Error Handling

Domain-level errors are raised in the service layer and mapped to HTTP responses
using centralized exception handlers.

Error responses follow a consistent structure and include a request identifier
to support traceability and debugging.

Unhandled exceptions are logged and returned as generic server errors without leaking internal details.

---

## Logging and Observability

Each request is assigned a unique request ID and logged with:

- HTTP method
- Path
- Status code
- Duration in milliseconds

Logging is intentionally minimal but sufficient to understand request flow,
latency, and failure modes without introducing heavy external dependencies.

---

## Testing

The test suite includes:

- Centralized database fixtures
- Dependency overrides for database sessions
- Isolated and repeatable test runs
- API-level tests covering core workflows

Tests are designed to validate behavior end-to-end while keeping setup explicit
and avoiding hidden state.

---

## Running the Application

### Local development

```bash
uvicorn accounting_api.app.main:app --reload
```

### Using Docker

```bash
docker build -t accounting-api .
docker run -p 8000:8000 accounting-api
```

---

## Configuration

Configuration is environment-driven and managed via Pydantic settings.
A `.env` file may be used for local development, while production environments
are expected to provide variables explicitly.

---

## Notes

This project intentionally avoids unnecessary complexity:

- No premature async database usage
- No heavyweight authentication frameworks
- No hidden magic or framework-specific abstractions

The goal is to keep the system easy to reason about, easy to test,
and easy to extend as requirements evolve.

---
