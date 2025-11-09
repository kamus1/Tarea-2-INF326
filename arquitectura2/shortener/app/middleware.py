import time
from collections import defaultdict

from litestar.middleware.base import AbstractMiddleware, DefineMiddleware
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_429_TOO_MANY_REQUESTS

from .config import RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS


class RateLimiterMiddleware(AbstractMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.max_requests = RATE_LIMIT_MAX_REQUESTS
        self.window = RATE_LIMIT_WINDOW_SECONDS
        self._clients: dict[str, list[float]] = defaultdict(list)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        client = scope.get("client")
        ip = client[0] if client else "unknown"
        now = time.time()

        timestamps = [t for t in self._clients.get(ip, []) if t > now - self.window]

        if len(timestamps) >= self.max_requests:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
            )

        timestamps.append(now)
        self._clients[ip] = timestamps
        await self.app(scope, receive, send)


rate_limiter_middleware = DefineMiddleware(RateLimiterMiddleware)
