import logging

from litestar import Litestar
import uvicorn

from arquitectura1.shortener.app.config import (
    DB_PATH,
    HTTP_HOST,
    HTTP_PORT,
    SSL_CERT_PATH,
    SSL_KEY_PATH,
)
from arquitectura1.shortener.app.database import init_db
from arquitectura1.shortener.app.routes import shorten_url, redirect_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("shortener.main")

# create app de litestar
def create_app() -> Litestar:
    logger.debug("Creando instancia de la aplicación Litestar")
    return Litestar(route_handlers=[shorten_url, redirect_url])

# main
if __name__ == "__main__":
    logger.info("Inicializando base de datos en %s", DB_PATH)
    try:
        init_db()
    except Exception:
        logger.exception("Fallo al inicializar la base de datos")
        raise

    app = create_app()

    if not SSL_CERT_PATH.exists() or not SSL_KEY_PATH.exists():
        logger.error(
            "Certificados TLS no encontrados. Ejecute 'python -m arquitectura1.shortener.generate_certs'"
        )
        raise FileNotFoundError("No se encontraron los certificados TLS requeridos.")
    logger.info(
        "shortener: servidor HTTP escuchando en %s:%s",
        HTTP_HOST,
        HTTP_PORT,
    )

    # run uvicorn
    uvicorn.run(
        app,
        host=HTTP_HOST,
        port=HTTP_PORT,
        log_level="info",
        ssl_certfile=str(SSL_CERT_PATH),
        ssl_keyfile=str(SSL_KEY_PATH),
    )
