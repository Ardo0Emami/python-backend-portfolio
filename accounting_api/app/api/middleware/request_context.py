from __future__ import annotations

import time
import uuid
import logging
from typing import Callable, Awaitable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

log = logging.getLogger("app")

REQUEST_ID_HEADER = "X-Request-Id"


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]]
            ) -> Response:
        request_id = request.headers.get(
            REQUEST_ID_HEADER) or str(uuid.uuid4()
                                      )
        start = time.perf_counter()

        # attach to request.state so handlers can access it
        request.state.request_id = request_id

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = int((time.perf_counter() - start) * 1000)
            log.exception(
                "Unhandled exception",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                },
            )
            raise

        duration_ms = int((time.perf_counter() - start) * 1000)
        response.headers[REQUEST_ID_HEADER] = request_id

        log.info(
            "request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response
