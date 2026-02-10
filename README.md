# Python Backend Portfolio

Welcome to my Python backend portfolio.

This repository contains a small set of focused backend projects, each designed to
demonstrate clean structure, correctness, and maintainable design in modern Python.
The emphasis is on explicit boundaries, predictable behavior, and production-oriented practices.

---

## Projects

- **[Accounting API](./accounting_api/)**  
  A realistic accounting backend built with FastAPI and SQLAlchemy.  
  Focus areas include layered architecture, explicit transaction handling,
  lightweight authentication, structured logging, and isolated testing.

- **[Python Data Structures](./data_structure/)**  
  Clean implementations of core data structures such as stacks, queues, and linked lists.  
  Each structure is fully tested, type-checked, and style-checked.

---

## Repository Structure

| Path | Description |
|------|-------------|
| `accounting_api/` | Accounting domain API (FastAPI + SQLAlchemy + Pydantic) |
| `data_structure/` | Core data structures with unit tests and static typing |
| `.vscode/` | Local development editor configuration |
| `dev.db` | Local development SQLite database |
| `README.md` | Repository overview and navigation |

---

## Technologies Used

- Python 3.11+
- FastAPI, Pydantic, SQLAlchemy 2.0
- `unittest` (data_structure)
- `pytest` (accounting_api)
- `flake8`, `mypy`
- Docker and environment-based configuration
- AsyncIO and background tasks where appropriate

---

## Highlights

- Clear separation of concerns across modules
- Type-safe, readable Python code
- Explicit transaction and session boundaries
- Deterministic and isolated tests
- Designed to be extended without hidden coupling

---

## Run Tests

```bash
pytest -q accounting_api/tests
python3 -m unittest discover -s data_structure -p 'test_*.py'
```

---

## Notes

Generated or local-only artifacts such as `htmlcov/`, `dev.db`, and editor configuration
are included for development convenience and are not required for production deployment.

---

## Connect

- GitHub: https://github.com/Ardo0Emami
- Email: it.arghavanemami@gmail.com