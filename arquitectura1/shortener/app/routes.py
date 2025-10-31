from litestar import get, post, Request, Response
from .service import create_short_url, resolve_hash
from .grpc_client import send_url_hit


# POST /shorten
# recibe una URL larga y devuelve su versión corta.
@post("/shorten")
async def shorten_url(request: Request) -> dict:
    data = await request.json()
    long_url = data["url"]
    _, short_hash = create_short_url(long_url) ## llama a create_short_url
    #return {"short_url": f"http://127.0.0.1:8000/{short_hash}", "hash": short_hash}
    #print("url acortado: ", "http://127.0.0.1:8000/" + short_hash)
    return {"short_url": f"http://127.0.0.1:8000/{short_hash}"}


# GET /{hash_str}
# redirige (302) a la URL original y notifica el evento al LogService.
@get("/{hash_str:str}")
async def redirect_url(hash_str: str) -> Response:
    long_url = resolve_hash(hash_str) ## llama a resolve_hash
    if not long_url:
        return Response(content="URL no encontrada", status_code=404)

    # notificar al log service sin bloquear la respuesta HTTP
    import threading
    threading.Thread(target=send_url_hit, args=(hash_str, long_url), daemon=True).start()

    # responder con 302 (redirect temporal)
    return Response(status_code=302, headers={"Location": long_url})
