# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\init.py\redis_session_589513449fc3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\init\redis_session.py

import redis

from redisClient.redis_connection import RedisConnection


def start_redis_connection() -> redis:

    return RedisConnection().connect()
