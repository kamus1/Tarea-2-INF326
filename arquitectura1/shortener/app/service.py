import sqlite3
from .config import DB_PATH
import base62

# ------ service functions, son usadas en los endpoints ------- #

# inserta una url en la base de datos y retorna el id y el hash
def create_short_url(long_url: str) -> tuple[int, str]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # insertar con hash temporal
    cur.execute("INSERT INTO urls (hash, long_url) VALUES (?, ?);", ("__temp__", long_url))
    conn.commit()
    new_id = cur.lastrowid
    
    # se hace hash del new
    hash_str = base62.encode(new_id) ## encode usando el pybase62

    cur.execute("UPDATE urls SET hash=? WHERE id=?;", (hash_str, new_id))
    conn.commit()
    conn.close()
    return new_id, hash_str

# retorna la url original a partir del hash
def resolve_hash(hash_str: str) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT long_url FROM urls WHERE hash=?;", (hash_str,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
