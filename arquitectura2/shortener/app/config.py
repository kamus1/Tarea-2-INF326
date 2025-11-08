from pathlib import Path

# configuración general del servicio Shortener
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8001
SSL_CERT_PATH = Path("certs/server.crt")
SSL_KEY_PATH = Path("certs/server.key")
BASE_URL = "https://localhost:8001"

# ruta de la base de datos local
DB_PATH = Path(__file__).resolve().parent.parent / "shortener.db" # base de datos del shortener service

# ID inicial
INITIAL_ID = 597652313

# configuración rate limiter
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 30

# configuración de cache
CACHE_MAX_ENTRIES = 1000
CACHE_TTL_SECONDS = 300
