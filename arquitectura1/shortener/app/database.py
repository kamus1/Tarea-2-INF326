import logging
import sqlite3

from .config import DB_PATH, INITIAL_ID

logger = logging.getLogger(__name__)

# se inicializa la base de datos
def init_db():
    logger.debug("init_db: conectando a la base de datos %s", DB_PATH)
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
        logger.debug("init_db: filas existentes en urls=%s", count)
        if count == 0:
            logger.debug("init_db: estableciendo secuencia inicial en %s", INITIAL_ID)
            cur.execute("DELETE FROM sqlite_sequence WHERE name='urls';")
            cur.execute(
                "INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', ?);",
                (INITIAL_ID - 1,),
            )
            conn.commit()

        logger.info("init_db: base de datos inicializada correctamente")
    except Exception:
        logger.exception("init_db: error al inicializar la base de datos")
        raise
    finally:
        conn.close()
        logger.debug("init_db: conexión cerrada")

# inserta una url en la base de datos
def insert_url(hash_str: str, long_url: str) -> int:
    logger.debug("insert_url: almacenando hash=%s long_url=%s", hash_str, long_url)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO urls (hash, long_url) VALUES (?, ?);",
            (hash_str, long_url),
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.info(
            "insert_url: fila creada con id=%s hash=%s",
            new_id,
            hash_str,
        )
        return new_id
    except Exception:
        logger.exception(
            "insert_url: error al insertar hash=%s long_url=%s",
            hash_str,
            long_url,
        )
        raise
    finally:
        conn.close()
        logger.debug("insert_url: conexión cerrada")


# obtiene la url original a partir del hash
def get_long_url(hash_str: str) -> str | None:
    logger.debug("get_long_url: buscando hash=%s", hash_str)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT long_url FROM urls WHERE hash = ?;", (hash_str,))
        row = cur.fetchone()
        if row:
            logger.info("get_long_url: encontrado hash=%s", hash_str)
        else:
            logger.warning("get_long_url: hash=%s no encontrado", hash_str)
        return row[0] if row else None
    except Exception:
        logger.exception("get_long_url: error al consultar hash=%s", hash_str)
        raise
    finally:
        conn.close()
        logger.debug("get_long_url: conexión cerrada")
