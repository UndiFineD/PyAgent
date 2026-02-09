# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\env.py
from dotenv import load_dotenv

load_dotenv()

from .telemetry.log import bound_logging_vars, get_logger, get_logging_contextvars
from .util.config import DEFAULT_CORE_CONFIG, DEFAULT_PROJECT_CONFIG

LOG = get_logger(DEFAULT_CORE_CONFIG.logging_format)

LOG.info(f"Default Core Config: [{DEFAULT_CORE_CONFIG}]")
LOG.info(f"Default Project Config: [{DEFAULT_PROJECT_CONFIG}]")
