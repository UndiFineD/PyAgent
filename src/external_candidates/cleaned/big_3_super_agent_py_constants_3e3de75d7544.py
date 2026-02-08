# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\big_3_super_agent.py\claude.py\hooks.py\utils.py\constants_3e3de75d7544.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\big-3-super-agent\.claude\hooks\utils\constants.py

#!/usr/bin/env -S uv run --script

# /// script

# requires-python = ">=3.8"

# ///

"""

Constants for Claude Code Hooks.

"""

import os

from pathlib import Path

# Base directory for all logs

# Default is 'logs' in the current working directory

LOG_BASE_DIR = os.environ.get("CLAUDE_HOOKS_LOG_DIR", "logs")


def get_session_log_dir(session_id: str) -> Path:
    """

    Get the log directory for a specific session.

    Args:

        session_id: The Claude session ID

    Returns:

        Path object for the session's log directory

    """

    return Path(LOG_BASE_DIR) / session_id


def ensure_session_log_dir(session_id: str) -> Path:
    """

    Ensure the log directory for a session exists.

    Args:

        session_id: The Claude session ID

    Returns:

        Path object for the session's log directory

    """

    log_dir = get_session_log_dir(session_id)

    log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir
