import json
import logging
import threading

from litestar import Request, Response, get, post

from .config import HTTP_HOST, HTTP_PORT
from .grpc_client import send_url_hit
from .service import create_short_url, resolve_hash

logger = logging.getLogger(__name__)


# POST /shorten
# recibe una URL larga y devuelve su versión corta.
@post("/shorten")
async def shorten_url(request: Request) -> Response | dict:
    logger.info("POST /shorten recibido")
    try:
        data = await request.json()
        logger.debug("POST /shorten payload=%s", json.dumps(data, ensure_ascii=False))
    except Exception:
        logger.exception("POST /shorten: error al parsear JSON")
        return Response(content="Payload inválido: no es JSON", status_code=400)

    long_url = data.get("url")
    if not long_url:
        logger.warning("POST /shorten: payload sin campo 'url': %s", data)
        return Response(content="El campo 'url' es obligatorio", status_code=400)

    try:
        _, short_hash = create_short_url(long_url)  # llama a create_short_url
    except Exception as exc:
        logger.exception("POST /shorten: error al crear hash para %s", long_url)
        return Response(
            content=f"Error interno al crear hash: {exc}",
            status_code=500,
        )

    short_url = f"http://{HTTP_HOST}:{HTTP_PORT}/{short_hash}"
    logger.info(
        "POST /shorten: url=%s acortada a %s (hash=%s)",
        long_url,
        short_url,
        short_hash,
    )
    return {"short_url": short_url}


# GET /{hash_str}
# redirige (302) a la URL original y notifica el evento al LogService.
@get("/{hash_str:str}")
async def redirect_url(hash_str: str) -> Response:
    logger.info("GET /%s recibido", hash_str)
    try:
        long_url = resolve_hash(hash_str)  # llama a resolve_hash
    except Exception as exc:
        logger.exception("GET /%s: error al resolver hash", hash_str)
        return Response(
            content=f"Error interno al resolver hash: {exc}",
            status_code=500,
        )

    if not long_url:
        logger.warning("GET /%s: hash no encontrado", hash_str)
        return Response(content="URL no encontrada", status_code=404)

    # notificar al log service sin bloquear la respuesta HTTP
    try:
        threading.Thread(
            target=send_url_hit,
            args=(hash_str, long_url),
            daemon=True,
        ).start()
        logger.debug("GET /%s: notificación a log_service despachada", hash_str)
    except Exception:
        logger.exception("GET /%s: error al notificar al log service", hash_str)

    # responder con 302 (redirect temporal)
    try:
        response = Response(
            content="",
            status_code=302,
            headers={"Location": long_url},
        )
    except Exception as exc:
        logger.exception("GET /%s: error al construir respuesta de redirección", hash_str)
        return Response(
            content=f"Error interno al redirigir: {exc}",
            status_code=500,
        )

    logger.info("GET /%s: redirigiendo a %s", hash_str, long_url)
    return response
