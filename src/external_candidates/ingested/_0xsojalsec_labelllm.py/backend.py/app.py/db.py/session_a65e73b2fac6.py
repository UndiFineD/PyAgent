# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\db\session.py
from app.core.config import settings
from motor import motor_asyncio
from redis.asyncio import Redis

# mongo session
mongo_session = motor_asyncio.AsyncIOMotorClient(settings.MongoDB_DSN)

# redis session
redis_session = Redis.from_url(str(settings.REDIS_DSN))
