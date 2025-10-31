from pathlib import Path

# configuración general del servicio Shortener
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8000

# dirección del servidor gRPC (LogService)
GRPC_ADDRESS = "127.0.0.1:50051"

# ruta de la base de datos local
DB_PATH = Path(__file__).resolve().parent.parent / "shortener.db" # base de datos del shortener service

# ID inicial
INITIAL_ID = 597652313
