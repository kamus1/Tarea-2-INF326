import sqlite3
from .config import DB_PATH, INITIAL_ID

# se inicializa la base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        );
    """)
    conn.commit()

    # asegurar que el autoincremento comience desde INITIAL_ID
    cur.execute("SELECT COUNT(*) FROM urls;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("DELETE FROM sqlite_sequence WHERE name='urls';")
        cur.execute(
            "INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', ?);",
            (INITIAL_ID - 1,),
        )
        conn.commit()

    conn.close()

# inserta una url en la base de datos
def insert_url(hash_str: str, long_url: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO urls (hash, long_url) VALUES (?, ?);",
        (hash_str, long_url),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


# obtiene la url original a partir del hash
def get_long_url(hash_str: str) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT long_url FROM urls WHERE hash = ?;", (hash_str,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
