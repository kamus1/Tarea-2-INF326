import logging
import base62

from .database import (
    get_long_url,
    insert_placeholder,
    update_hash_for_id,
)

logger = logging.getLogger(__name__)

# ------ service functions, son usadas en los endpoints ------- #

# inserta una url en la base de datos y retorna el id y el hash
def create_short_url(long_url: str) -> tuple[int, str]:
    logger.info("create_short_url: procesando long_url=%s", long_url)
    try:
        new_id = insert_placeholder(long_url)
        logger.debug("create_short_url: id provisional=%s", new_id)

        hash_str = base62.encode(new_id)
        logger.debug("create_short_url: hash generado=%s", hash_str)

        update_hash_for_id(new_id, hash_str)
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

# retorna la url original a partir del hash
def resolve_hash(hash_str: str) -> str | None:
    logger.info("resolve_hash: resolviendo hash=%s", hash_str)
    try:
        long_url = get_long_url(hash_str)
        if long_url:
            logger.info("resolve_hash: hash=%s resuelto con éxito", hash_str)
        else:
            logger.warning("resolve_hash: hash=%s no encontrado", hash_str)
        return long_url
    except Exception:
        logger.exception("resolve_hash: error al consultar hash=%s", hash_str)
        raise
