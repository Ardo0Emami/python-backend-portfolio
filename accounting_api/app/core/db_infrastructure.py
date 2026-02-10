from __future__ import annotations

from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Any
from sqlalchemy.engine.interfaces import DBAPIConnection


def make_engine(
    url: str,
    *,
    echo: bool = False,
    connect_args: dict[str, Any] | None = None,
    poolclass: type[Any] | None = None,
) -> Engine:
    if connect_args is None:
        connect_args = {}

    engine = create_engine(
        url,
        echo=echo,
        future=True,
        connect_args=connect_args,
        poolclass=poolclass,
    )

    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_conn: DBAPIConnection, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # # Add live SQL logger
    # @event.listens_for(engine, "before_cursor_execute")
    # def before_cursor_execute(
    #         conn: DBAPIConnection,
    #         cursor: Any,
    #         statement: str,
    #         parameters: dict[str, Any] | tuple[Any, ...],
    #         context: Any,
    #         executemany: bool
    #         ) -> None:
    #     print("\n----- SQL Executed -----")
    #     print(str(statement))
    #     if parameters:
    #         print("Params:", str(parameters))
    #     print("------------------------\n")

    return engine


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Return a configured session factory."""
    return sessionmaker(
               bind=engine,
               autoflush=False,
               autocommit=False,
               future=True
    )


@contextmanager
def session_scope(SessionFactory: sessionmaker[Session]):
    """
    Explicit transactional scope for non-HTTP contexts
    (scripts, admin jobs, migrations, educational usage).
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
