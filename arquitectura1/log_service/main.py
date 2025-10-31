from arquitectura1.log_service.app.database import init_db
from arquitectura1.log_service.app.server import serve

if __name__ == "__main__":
    init_db()
    serve()
