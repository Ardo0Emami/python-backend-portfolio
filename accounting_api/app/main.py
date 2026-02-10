from contextlib import asynccontextmanager
from fastapi import FastAPI
from accounting_api.app.core.db_adapter import engine
from accounting_api.app.models.sqlalchemy_models import Base
from accounting_api.app.api.errors import (
    invalid_operation_handler,
    not_found_handler,
    unhandled_exception_handler
)
from accounting_api.app.api.middleware.request_context import (
    RequestContextMiddleware
)
from accounting_api.app.api.routes import customers, invoices
from accounting_api.app.core.config import settings
from accounting_api.app.core.logging import setup_logging
from accounting_api.app.services.errors import (
    InvalidOperationError,
    NotFoundError
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables are created at startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


# middleware
app.add_middleware(RequestContextMiddleware)

setup_logging("DEBUG" if settings.debug else "INFO")

app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(InvalidOperationError, invalid_operation_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "ok",
        "docs": "/docs",
        "health": "/healthz",
    }


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


app.include_router(customers.router)
app.include_router(invoices.router)
