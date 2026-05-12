import asyncio
import json
import redis
from config import REDIS_URL

r = None
if REDIS_URL:
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True)
        r.ping()
    except Exception as e:
        print(f"⚠️ Redis não disponível - {e}")
        r = None

CACHE_TTL = 300  # 5 minutos


async def get_cached_hobbies(user_id: str) -> list[dict] | None:
    """Obtém hobbies do cache Redis."""
    if not r:
        return None
    
    def _get():
        key = f"user:{user_id}:hobbies"
        data = r.get(key)
        if data:
            return json.loads(data)
        return None
    
    return await asyncio.to_thread(_get)


async def set_cached_hobbies(user_id: str, hobbies: list[dict]):
    """Armazena hobbies no cache Redis."""
    if not r:
        return
    
    def _set():
        key = f"user:{user_id}:hobbies"
        r.set(key, json.dumps(hobbies, default=str), ex=CACHE_TTL)
    
    await asyncio.to_thread(_set)


async def invalidate_hobbies_cache(user_id: str):
    """Invalida o cache de hobbies."""
    if not r:
        return
    
    def _delete():
        key = f"user:{user_id}:hobbies"
        r.delete(key)
    
    await asyncio.to_thread(_delete)
