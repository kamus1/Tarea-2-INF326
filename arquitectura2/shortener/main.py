from litestar import Litestar
from app.database import init_db
from app.routes import routes
from app.middleware import rate_limiter_middleware
from app.config import SSL_CERT_PATH, SSL_KEY_PATH, HTTP_HOST, HTTP_PORT
import uvicorn


app = Litestar(route_handlers=routes, middleware=[rate_limiter_middleware])


if __name__ == "__main__":
    
    init_db()
    
    uvicorn.run(
        "main:app",
        host=HTTP_HOST,
        port=HTTP_PORT,
        ssl_certfile=str(SSL_CERT_PATH),
        ssl_keyfile=str(SSL_KEY_PATH),
    )