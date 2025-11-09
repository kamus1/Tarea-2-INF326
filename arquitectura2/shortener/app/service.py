import logging
import time
from typing import Optional

import base62

from .config import CACHE_MAX_ENTRIES, CACHE_TTL_SECONDS
from .database import (
    get_long_url,
    insert_placeholder,
    update_hash_for_id,
    url_exists,
)

logger = logging.getLogger(__name__)

# cache: dict hash -> (long_url, expire_ts)
_cache: dict[str, tuple[str, float]] = {}


def _evict_expired() -> None:
    now = time.time()
    expired = [key for key, (_, exp) in _cache.items() if exp <= now]
    for key in expired:
        _cache.pop(key, None)


def _set_cache(key: str, value: str) -> None:
    _evict_expired()

    if CACHE_MAX_ENTRIES and len(_cache) >= CACHE_MAX_ENTRIES:
        oldest_key = min(_cache.items(), key=lambda kv: kv[1][1])[0]
        _cache.pop(oldest_key, None)

    ttl = CACHE_TTL_SECONDS if CACHE_TTL_SECONDS and CACHE_TTL_SECONDS > 0 else None
    expires_at = time.time() + ttl if ttl else float("inf")
    _cache[key] = (value, expires_at)


def _get_cache(key: str) -> Optional[str]:
    _evict_expired()
    data = _cache.get(key)
    return data[0] if data else None


def create_short_url(long_url: str) -> tuple[int, str]:
    """Inserta una URL larga y retorna el (id, hash) correspondiente."""
    logger.info("create_short_url: procesando %s", long_url)

    if url_exists(long_url):
        logger.warning("create_short_url: URL ya existe, generando nuevo hash igualmente")

    row_id = insert_placeholder(long_url)
    logger.debug("create_short_url: id generado %s", row_id)

    hash_str = base62.encode(row_id)
    update_hash_for_id(row_id, hash_str)
    logger.info("create_short_url: hash %s asignado a id %s", hash_str, row_id)

    _set_cache(hash_str, long_url)
    return row_id, hash_str


def resolve_hash(hash_str: str) -> Optional[str]:
    """Obtiene la URL original a partir del hash."""
    cached = _get_cache(hash_str)
    if cached:
        logger.info("resolve_hash: cache hit hash=%s", hash_str)
        return cached

    logger.info("resolve_hash: cache miss hash=%s, consultando DB", hash_str)
    long_url = get_long_url(hash_str)
    if long_url:
        logger.info("resolve_hash: hash=%s encontrado en DB", hash_str)
        _set_cache(hash_str, long_url)
    else:
        logger.warning("resolve_hash: hash=%s no encontrado", hash_str)
    return long_url
