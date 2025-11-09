from litestar import post, get, Request, Response
from litestar.status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from app.service import create_short_url, resolve_hash


@post("/shorten")
async def shorten(request: Request) -> Response:
    data = await request.json()
    long_url = data.get("url") if isinstance(data, dict) else None
    if not long_url:
        return Response(content={"error": "missing 'url'"}, status_code=HTTP_400_BAD_REQUEST, media_type="applcation/json")

    short = create_short_url(long_url)
    return Response(content={"short_url": short}, status_code=HTTP_201_CREATED, media_type="application/json")


@get("/{hash:str}")
async def redirect_to_long(hash: str) -> Response:
    long_url = resolve_hash(hash)
    if not long_url:
        return Response(content={"error": "not found"}, status_code=404, media_type="application/json")
    return Response(content="", status_code=301, headers={"Location": long_url})


routes = [shorten, redirect_to_long]