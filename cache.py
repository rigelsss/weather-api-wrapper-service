import redis
import json
from config import REDIS_HOST, REDIS_PORT, CACHE_EXPIRATION_SECONDS

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get_cached_weather(city):
    key = city.strip().lower()
    cached_data = r.get(key)
    if cached_data is None:
        return None
    return json.loads(cached_data)

def set_cached_weather(city, weather_data):
    key = city.strip().lower()
    r.set(key, json.dumps(weather_data), ex=CACHE_EXPIRATION_SECONDS)
