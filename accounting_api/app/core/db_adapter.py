from typing import Generator
from sqlalchemy.orm import Session

from accounting_api.app.core.config import settings
from accounting_api.app.core.db_infrastructure import (
    make_engine,
    make_session_factory,
)

engine = make_engine(
    settings.database_url,
    echo=settings.echo_sql,
)

SessionLocal = make_session_factory(engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI database dependency defining the transactional boundary
    of the web application.

    NOTE:
    We intentionally do NOT use `session_scope(SessionLocal)` here.
    See architecture notes for rationale.
    """
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
