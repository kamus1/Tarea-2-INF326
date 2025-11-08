import ssl
import asyncio
from litestar import Litestar
from litestar.middleware import Middleware
from litestar.middleware.base import BaseHTTPMiddleware
from litestar.datastructures import State
import uvicorn

from app.config import DB_PATH, HTTP_HOST, HTTP_PORT
from app.database import init_db
from app.routes import routes
from app.config import SSL_CERT_PATH, SSL_KEY_PATH, DB_PATH, HTTP_HOST, HTTP_PORT


app = Litestar(route_handlers=routes)


if __name__ == "__main__":
    
    print("Inicializando base de datos en %s", DB_PATH)
    try:
        init_db()
    except Exception:
        print("Fallo al inicializar la base de datos")
        raise

    
    ssl_context = None
    try:
        # Si existen los archivos generados por generate_certs.py, uvicorn los usará
        ssl_context = {
            "ssl_certfile": SSL_CERT_PATH,
            "ssl_keyfile": SSL_KEY_PATH,
        }
    except Exception:
        ssl_context = None


# uvicorn acepta directamente certfile/keyfile args
uvicorn.run("main:app", host=HTTP_HOST, port=HTTP_PORT, reload=False, **(ssl_context or {}))