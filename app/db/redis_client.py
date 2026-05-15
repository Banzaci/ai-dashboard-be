import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or ""

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

SESSION_TTL = 60 * 30  # 30 minuter

def get_session(session_id: str) -> dict:
    data = r.get(f"session:{session_id}")
    if not data:
        return {"slots": {}, "pending_slot": None}
    return json.loads(str(data))

def save_session(session_id: str, session: dict):
    r.setex(f"session:{session_id}", SESSION_TTL, json.dumps(session))

def delete_session(session_id: str):
    r.delete(f"session:{session_id}")