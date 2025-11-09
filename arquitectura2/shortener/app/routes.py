import logging

from litestar import Request, Response, get, post
from litestar.status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .config import BASE_URL
from .service import create_short_url, resolve_hash

logger = logging.getLogger(__name__)


@post("/shorten")
async def shorten(request: Request) -> Response:
    try:
        data = await request.json()
    except Exception:
        return Response(
            content={"error": "payload must be valid JSON"},
            status_code=HTTP_400_BAD_REQUEST,
            media_type="application/json",
        )

    long_url = data.get("url") if isinstance(data, dict) else None
    if not long_url:
        return Response(
            content={"error": "missing 'url'"},
            status_code=HTTP_400_BAD_REQUEST,
            media_type="application/json",
        )

    try:
        _, short_hash = create_short_url(long_url)
    except Exception as exc:
        logger.exception("shorten: error al crear hash para %s", long_url)
        return Response(
            content={"error": f"internal error: {exc}"},
            status_code=500,
            media_type="application/json",
        )

    short_url = f"{BASE_URL}/{short_hash}"
    return Response(
        content={"short_url": short_url},
        status_code=HTTP_201_CREATED,
        media_type="application/json",
    )


@get("/{hash:str}")
async def redirect_to_long(hash: str) -> Response:
    try:
        long_url = resolve_hash(hash)
    except Exception as exc:
        logger.exception("redirect_to_long: error al resolver hash %s", hash)
        return Response(
            content={"error": f"internal error: {exc}"},
            status_code=500,
            media_type="application/json",
        )

    if not long_url:
        return Response(
            content={"error": "not found"},
            status_code=HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    return Response(content="", status_code=301, headers={"Location": long_url})


routes = [shorten, redirect_to_long]
