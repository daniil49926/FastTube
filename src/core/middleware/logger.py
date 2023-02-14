from logging import Logger

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        self.logger.info(
            response.status_code,
            extra={
                "client_ip": request.client.host,
                "method": request.method,
                "url": request.url,
            },
        )
        return response
