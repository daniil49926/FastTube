import time

import aiohttp
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from core.settings import settings


class AnalyticsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start: float = time.time()
        response = await call_next(request)
        process_time = time.time() - start

        data_on_analyze: str = "REQUEST-{}-{}-{};RESPONSE-{}".format(
            request.method, request.url, process_time, response.status_code
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.ANALYTICS_SERVER_URL}/send-analytics", data=data_on_analyze
            ) as _:
                pass

        return response
