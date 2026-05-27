import time
import traceback
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..core.logger import get_logger

logger = get_logger("http.request")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        structlog.contextvars.clear_contextvars()
        
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else ""
        )

        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            structlog.contextvars.bind_contextvars(
                status_code=response.status_code, 
                duration_ms=round(process_time * 1000, 2)
            )
            
            if response.status_code >= 500:
                logger.error("HTTP Request Failed")
            elif response.status_code >= 400:
                logger.warning("HTTP Request Client Error")
            else:
                logger.info("HTTP Request Success")
                
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            process_time = time.time() - start_time
            structlog.contextvars.bind_contextvars(
                status_code=500, 
                duration_ms=round(process_time * 1000, 2)
            )
            logger.error("HTTP Request Unhandled Exception", exc_info=exc)
            raise
