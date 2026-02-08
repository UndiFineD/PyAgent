# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\utils.py\log_exception_context_manager_1373386d092d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\utils\log_exception_context_manager.py

import logging

from contextlib import contextmanager


@contextmanager
def raise_exception():

    try:
        yield

    except Exception as err:
        logging.exception(err)

        raise


@contextmanager
def log_exception():

    try:
        yield

    except Exception as err:
        logging.exception(err)
