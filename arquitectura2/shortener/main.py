import uvicorn
from litestar import Litestar

from arquitectura2.shortener.app.config import (
    HTTP_HOST,
    HTTP_PORT,
    SSL_CERT_PATH,
    SSL_KEY_PATH,
)
from arquitectura2.shortener.app.database import init_db
from arquitectura2.shortener.app.middleware import rate_limiter_middleware
from arquitectura2.shortener.app.routes import routes


app = Litestar(route_handlers=routes, middleware=[rate_limiter_middleware])


if __name__ == "__main__":
    init_db()

    uvicorn.run(
        app,
        host=HTTP_HOST,
        port=HTTP_PORT,
        ssl_certfile=str(SSL_CERT_PATH),
        ssl_keyfile=str(SSL_KEY_PATH),
    )
