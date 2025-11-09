from pathlib import Path

# configuración general del servicio Shortener
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8001
CERTS_DIR = Path(__file__).resolve().parent.parent / "certs"
SSL_CERT_PATH = CERTS_DIR / "server.crt"
SSL_KEY_PATH = CERTS_DIR / "server.key"
BASE_URL = f"https://{HTTP_HOST}:{HTTP_PORT}"

# ruta de la base de datos local
DB_PATH = Path(__file__).resolve().parent.parent / "shortener.db"  # base de datos del shortener service

# ID inicial
INITIAL_ID = 597652313

# configuración rate limiter
RATE_LIMIT_WINDOW_SECONDS = 15 # ventana de tiempo
RATE_LIMIT_MAX_REQUESTS = 3 # cantidad de request maximas 

# configuración de cache
CACHE_MAX_ENTRIES = 1000
CACHE_TTL_SECONDS = 300
