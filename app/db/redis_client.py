import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or ""

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)