# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\util.py\generate_ids_275fb2574277.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\util\generate_ids.py

import uuid

from functools import wraps

from typing import final

from ..env import LOG, bound_logging_vars


def generate_temp_id() -> str:

    return uuid.uuid4().hex


def track_process(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):

        func_name = func.__name__

        use_id = generate_temp_id()

        with bound_logging_vars(temp_id=use_id, func_name=func_name):
            LOG.info(f"Enter {func_name}")

            try:
                return await func(*args, **kwargs)

            finally:
                LOG.info(f"Exit {func_name}")

    return wrapper
