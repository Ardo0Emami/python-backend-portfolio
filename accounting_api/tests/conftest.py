from __future__ import annotations

from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Transaction
from sqlalchemy.pool import StaticPool

from accounting_api.app.core.db_infrastructure import (
    make_engine,
    make_session_factory
)
from accounting_api.app.models.sqlalchemy_models import Base
from accounting_api.app.core.db_adapter import get_db  # dependency to override
import accounting_api.app.core.db_adapter as db_adapter
import accounting_api.app.main as main
from accounting_api.app.core.config import settings


""""
assert settings.environment == "test"
"""
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

# Test DB Engine (single in-memory database for the entire test run)
TEST_ENGINE = make_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = make_session_factory(TEST_ENGINE)


# Ensure the app uses the test engine (important if main.py does create_all on startup)
@pytest.fixture(scope="session", autouse=True)
def _wire_app_to_test_engine() -> Generator[None, Any, None]:
    # Patch any module-level engine references used by the app
    db_adapter.engine = TEST_ENGINE
    db_adapter.SessionLocal = TestSessionLocal
    main.engine = TEST_ENGINE

    yield

    # Nothing to undo strictly required for pytest process exit


# Create schema once per test session
@pytest.fixture(scope="session", autouse=True)
def _create_test_schema() -> Generator[None, Any, None]:
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


# DB session per test:
#   - One outer transaction per test (rollback at teardown)
#   - One SAVEPOINT (nested transaction) that automatically restarts
@pytest.fixture()
def test_db_session() -> Generator[Session, Any, None]:
    with TEST_ENGINE.connect() as connection:
        outer_tx = connection.begin()

        session: Session = TestSessionLocal(bind=connection)

        # Start SAVEPOINT so code under test can call session.commit() safely
        session.begin_nested()

        @event.listens_for(session, "after_transaction_end")
        def _restart_savepoint(sess: Session, trans: Transaction) -> None:
            """
            If the nested transaction(SAVEPOINT)
            ends (e.g. via sess.commit()),
            restart it as long as we are still
            inside the outer transaction.
            """
            if trans.nested and trans._parent is not None and not trans._parent.nested:
                sess.begin_nested()

        try:
            yield session
        finally:
            # Prevent event listener accumulation in long-running runs
            event.remove(session, "after_transaction_end", _restart_savepoint)

            session.close()
            outer_tx.rollback()  # restore pristine state for next test


# FastAPI client with dependency override
@pytest.fixture()
def client(test_db_session: Session) -> Generator[TestClient, Any, None]:
    def override_get_db() -> Generator[Session, Any, None]:
        yield test_db_session

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main.app) as c:
        yield c
    main.app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    """
    Standard auth headers for protected endpoints.
    """
    return {"X-API-Key": settings.api_key}
