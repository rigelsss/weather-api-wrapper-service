import os
from dotenv import load_dotenv

load_dotenv()

VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

CACHE_EXPIRATION_SECONDS = 12 * 60 * 60  # 12 hours

if not VISUAL_CROSSING_API_KEY:
    raise RuntimeError("VISUAL_CROSSING_API_KEY is not set in the environment variables.")