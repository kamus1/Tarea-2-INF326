import logging
import sqlite3

import base62

from .config import DB_PATH

logger = logging.getLogger(__name__)

# ------ service functions, son usadas en los endpoints ------- #

# inserta una url en la base de datos y retorna el id y el hash
def create_short_url(long_url: str) -> tuple[int, str]:
    logger.info("create_short_url: procesando long_url=%s", long_url)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        # insertar con hash temporal
        cur.execute(
            "INSERT INTO urls (hash, long_url) VALUES (?, ?);",
            ("__temp__", long_url),
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.debug("create_short_url: id provisional=%s", new_id)

        # se hace hash del new
        hash_str = base62.encode(new_id)  # encode usando el pybase62
        logger.debug("create_short_url: hash generado=%s", hash_str)

        cur.execute("UPDATE urls SET hash=? WHERE id=?;", (hash_str, new_id))
        conn.commit()
        logger.info(
            "create_short_url: url almacenada con id=%s hash=%s",
            new_id,
            hash_str,
        )
        return new_id, hash_str
    except Exception:
        logger.exception(
            "create_short_url: error al procesar long_url=%s",
            long_url,
        )
        raise
    finally:
        conn.close()
        logger.debug("create_short_url: conexión cerrada")

# retorna la url original a partir del hash
def resolve_hash(hash_str: str) -> str | None:
    logger.info("resolve_hash: resolviendo hash=%s", hash_str)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT long_url FROM urls WHERE hash=?;", (hash_str,))
        row = cur.fetchone()
        if row:
            logger.info("resolve_hash: hash=%s resuelto con éxito", hash_str)
        else:
            logger.warning("resolve_hash: hash=%s no encontrado", hash_str)
        return row[0] if row else None
    except Exception:
        logger.exception("resolve_hash: error al consultar hash=%s", hash_str)
        raise
    finally:
        conn.close()
        logger.debug("resolve_hash: conexión cerrada")
