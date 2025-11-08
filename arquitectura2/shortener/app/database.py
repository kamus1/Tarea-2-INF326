import sqlite3

from .config import DB_PATH, INITIAL_ID


# se inicializa la base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                long_url TEXT NOT NULL
            );
            """
        )
        conn.commit()

        # asegurar que el autoincremento comience desde INITIAL_ID
        cur.execute("SELECT COUNT(*) FROM urls;")
        count = cur.fetchone()[0]
        if count == 0:
            print("init_db: estableciendo secuencia inicial en %s", INITIAL_ID)
            cur.execute("DELETE FROM sqlite_sequence WHERE name='urls';")
            cur.execute(
                "INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', ?);",
                (INITIAL_ID - 1,),
            )
            conn.commit()

    except Exception:
        raise
    
    finally:
        conn.close()
        
def new_id(long_url: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM urls WHERE long_url = ?;", long_url)
        conn.commit()
        if cur.fetchone():
            return -1
        cur.execute("INSERT INTO urls (hash, long_url) VALUES (?, ?);", ("__temp__", long_url))
        conn.commit()
        new_id = cur.lastrowid
        return new_id
    except Exception:
        raise
    finally:
        conn.close()

# inserta una url en la base de datos
def insert_url(id: int, hash_str: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("UPDATE urls SET hash=? WHERE id=?;", (hash_str, id))
        conn.commit()
    
    except Exception:
        raise
    
    finally:
        conn.close()


# obtiene la url original a partir del hash
def get_long_url(hash_str: str) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT long_url FROM urls WHERE hash = ?;", (hash_str,))
        row = cur.fetchone()
        return row[0] if row else None

    except Exception:
        raise

    finally:
        conn.close()
