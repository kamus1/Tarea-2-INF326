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

# inserta una url con hash temporal y retorna el id generado
def insert_placeholder(long_url: str) -> int:
    logger.debug("insert_placeholder: creando registro temporal para %s", long_url)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO urls (hash, long_url) VALUES (?, ?);",
            ("__temp__", long_url),
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.info(
            "insert_placeholder: fila creada con id=%s",
            new_id,
        )
        return new_id
    except Exception:
        logger.exception(
            "insert_placeholder: error al insertar long_url=%s",
            long_url,
        )
        raise
    finally:
        conn.close()
        logger.debug("insert_placeholder: conexión cerrada")


# actualiza el hash definitivo asociado a un id
def update_hash_for_id(row_id: int, hash_str: str) -> None:
    logger.debug("update_hash_for_id: id=%s hash=%s", row_id, hash_str)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE urls SET hash=? WHERE id=?;",
            (hash_str, row_id),
        )
        conn.commit()
        logger.info("update_hash_for_id: hash actualizado para id=%s", row_id)
    except Exception:
        logger.exception(
            "update_hash_for_id: error al actualizar id=%s hash=%s",
            row_id,
            hash_str,
        )
        raise
    finally:
        conn.close()
        logger.debug("update_hash_for_id: conexión cerrada")


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
