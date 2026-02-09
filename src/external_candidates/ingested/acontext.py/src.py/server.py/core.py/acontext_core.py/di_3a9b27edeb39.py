# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\di.py
from . import service
from .env import DEFAULT_CORE_CONFIG, LOG
from .infra.async_mq import MQ_CLIENT, close_mq, init_mq
from .infra.db import DB_CLIENT, close_database, init_database
from .infra.redis import REDIS_CLIENT, close_redis, init_redis
from .infra.s3 import S3_CLIENT, close_s3, init_s3
from .llm.complete import llm_sanity_check
from .llm.embeddings import embedding_sanity_check


async def setup() -> None:
    # await llm_sanity_check()
    # await embedding_sanity_check()
    await init_database()
    await init_redis()
    await init_s3()
    await init_mq()


async def cleanup() -> None:
    await close_database()
    await close_redis()
    await close_s3()
    await close_mq()
