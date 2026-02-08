# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\logger.py\logger_b1cdef161126.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\logger\logger.py

import sys

from loguru import logger


def init_logger():
    logger.remove()

    # scheduler log

    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS zz}</green> | <light-blue>scheduler</light-blue> | {level} | <level>{message}</level>",
        filter="app.scheduler",
    )

    # web middleware log

    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS zz}</green> | <light-blue>middleware</light-blue> | {level} | {extra[request_id]} | <level>{message}</level>",
        filter="app.middleware",
    )

    # web log

    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS zz}</green> | <light-blue>server</light-blue> | {level} | {extra[request_id]} | <level>{message}</level>",
        filter="app.api",
    )
