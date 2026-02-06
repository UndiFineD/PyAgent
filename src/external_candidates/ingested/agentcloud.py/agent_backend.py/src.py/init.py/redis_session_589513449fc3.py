# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\init\redis_session.py
import redis
from redisClient.redis_connection import RedisConnection


def start_redis_connection() -> redis:
    return RedisConnection().connect()
