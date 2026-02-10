from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from accounting_api.app.services.errors import (
    NotFoundError,
    InvalidOperationError
)


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "type": "not_found",
                "message": str(exc),
                "request_id": _request_id(request),
            }
        },
    )


def invalid_operation_handler(request: Request, exc: InvalidOperationError):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "type": "invalid_operation",
                "message": str(exc),
                "request_id": _request_id(request),
            }
        },
    )


def unhandled_exception_handler(request: Request, exc: Exception):
    # Don’t leak internal details
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "Internal server error",
                "request_id": _request_id(request),
            }
        },
    )
