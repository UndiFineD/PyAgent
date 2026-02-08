# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_x_anylabeling_server.py\app.py\core.py\logging_d7de1292613d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\core\logging.py

import sys

from datetime import datetime

from pathlib import Path

from loguru import logger

from .config import LoggingConfig


def setup_logging(config: LoggingConfig):
    """Configure loguru logger based on settings.

    Args:

        config: Logging configuration.

    """

    logger.remove()

    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=console_format,
        level=config.console_level,
        colorize=True,
    )

    if config.file_enabled:
        if config.file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            file_path = f"logs/server_{timestamp}.log"

        else:
            file_path = config.file_path

        log_path = Path(file_path)

        log_path.parent.mkdir(parents=True, exist_ok=True)

        if config.format == "json":
            logger.add(
                file_path,
                format="{time} {level} {name} {function} {message}",
                level=config.level,
                rotation=config.rotation,
                retention=config.retention,
                serialize=True,
            )

        else:
            logger.add(
                file_path,
                format=console_format,
                level=config.level,
                rotation=config.rotation,
                retention=config.retention,
            )
