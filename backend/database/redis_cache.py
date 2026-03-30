import json
import redis
from config import REDIS_URL

r = redis.from_url(REDIS_URL, decode_responses=True)

CACHE_TTL = 300  # 5 minutos


def get_cached_hobbies(user_id: str) -> list[dict] | None:
    key = f"user:{user_id}:hobbies"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None


def set_cached_hobbies(user_id: str, hobbies: list[dict]):
    key = f"user:{user_id}:hobbies"
    r.set(key, json.dumps(hobbies, default=str), ex=CACHE_TTL)


def invalidate_hobbies_cache(user_id: str):
    key = f"user:{user_id}:hobbies"
    r.delete(key)
