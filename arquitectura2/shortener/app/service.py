from typing import Optional
from app.database import insert_url, get_long_url, new_id
from app.config import CACHE_MAX_ENTRIES, CACHE_TTL_SECONDS
import time
import base62



#cache: dict hash -> (long_url, expire_ts)
_cache = {}


def _evict_expired():
    now = time.time()
    keys = [k for k, (_, exp) in _cache.items() if exp <= now]
    for k in keys:
        _cache.pop(k, None)


def _set_cache(key: str, value: str):
    _evict_expired()
    
    if len(_cache) >= CACHE_MAX_ENTRIES:
        oldest = min(_cache.items(), key=lambda kv: kv[1][1])[0]
        _cache.pop(oldest, None)
        _cache[key] = (value, time.time() + CACHE_TTL_SECONDS)


def _get_cache(key: str) -> Optional[str]:
    _evict_expired()
    val = _cache.get(key)
    return val[0] if val else None

# inserta una url en la base de datos y retorna el id y el hash
def create_short_url(long_url: str) -> tuple[int, str]:
    id = new_id(long_url)
    if id == -1:
        raise ValueError("URL ya existe")
    hash_str = base62.encode(id)
    insert_url(id, hash_str)
    _set_cache(hash_str, long_url)
    return id, hash_str


# retorna la url original a partir del hash
def resolve_hash(hash_str: str) -> str | None:
    cached = _get_cache(hash_str)
    if cached:
        return cached
    
    url = get_long_url(hash_str)
    if url:
        _set_cache(hash_str, url)
        
    return url