# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\telemetry\log.py
import logging
import sys

import structlog

from ..util.terminal_color import TerminalColorMarks

bound_logging_vars = structlog.contextvars.bound_contextvars


def get_logging_contextvars():
    return structlog.contextvars.get_contextvars()


def __get_json_logger():
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PATHNAME,
            ]
        ),
    ]

    structlog_processors = shared_processors + [
        structlog.processors.dict_tracebacks,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger("acontext-core")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def __get_text_logger():
    logger = logging.getLogger("acontext-core")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        f"{TerminalColorMarks.BOLD}{TerminalColorMarks.BLUE}>{TerminalColorMarks.END} %(asctime)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_logger(format="text") -> logging.Logger:
    if format == "json":
        LOG = __get_json_logger()
    else:
        LOG = __get_text_logger()
    return LOG
