import sqlite3
from pathlib import Path

# se define el path de la base de datos
DB_PATH = Path(__file__).resolve().parent.parent / "log.db" # la base de datos de log service

# funcion para inicializar la base de datos
# crea la tabla hits si no existe
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT NOT NULL,
            long_url TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# funcion para insertar un hit en la base de datos
def insert_hit(hash_str: str, long_url: str, timestamp: str):
    #conectarse
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # insertar el hit en la tabla hits
    cur.execute(
        "INSERT INTO hits (hash, long_url, timestamp) VALUES (?, ?, ?);",
        (hash_str, long_url, timestamp),
    )

    # confirmar los cambios
    conn.commit()
    conn.close()
