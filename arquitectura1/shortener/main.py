from arquitectura1.shortener.app.database import init_db
from arquitectura1.shortener.app.routes import shorten_url, redirect_url
from arquitectura1.shortener.app.config import HTTP_HOST, HTTP_PORT
from litestar import Litestar
import uvicorn

# create app de litestar
def create_app() -> Litestar:
    return Litestar(route_handlers=[shorten_url, redirect_url])

# main
if __name__ == "__main__":
    init_db()
    app = create_app()
    print(f"shortener: servidor HTTP escuchando en {HTTP_HOST}:{HTTP_PORT}")

    # run uvicorn
    uvicorn.run(app, host=HTTP_HOST, port=HTTP_PORT, log_level="info")
