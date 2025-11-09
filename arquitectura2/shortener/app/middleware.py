from litestar.middleware.base import DefineMiddleware, AbstractMiddleware
from litestar.connection import Request
from litestar.response import Response
from litestar.status_codes import HTTP_429_TOO_MANY_REQUESTS
from app.config import RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS
import time


class RateLimiterMiddleware(AbstractMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.max_requests = RATE_LIMIT_MAX_REQUESTS
        self.window = RATE_LIMIT_WINDOW_SECONDS
        self._clients = {}


    async def before_request(self, request: Request) -> None:
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        timestamps = [t for t in self._clients.get(ip, []) if t > now - self.window]


        if len(timestamps) >= self.max_requests:
            raise Response(
                content={"error": "rate limit exceeded"},
                status_code=HTTP_429_TOO_MANY_REQUESTS
            )

        timestamps.append(now)
        self._clients[ip] = timestamps

rate_limiter_middleware = DefineMiddleware(RateLimiterMiddleware)