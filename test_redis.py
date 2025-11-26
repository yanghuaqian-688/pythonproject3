# test_redis.py
import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    client = redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    pong = client.ping()
    print("Redis connection successful:", pong)
except Exception as e:
    print("Redis connection failed:", e)