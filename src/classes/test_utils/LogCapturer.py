#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Any, List, Optional
import logging

class LogCapturer:
    """Captures logging output for testing."""

    def __init__(self, level: int = logging.INFO) -> None:
        """Initialize log capturer."""
        self.level = level
        self.logs: List[logging.LogRecord] = []
        self.handler = logging.Handler()
        self.handler.emit = lambda record: self.logs.append(record)

    def __enter__(self) -> "LogCapturer":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.stop()

    def start(self) -> None:
        """Start capturing logs."""
        root_logger = logging.getLogger()
        root_logger.addHandler(self.handler)
        root_logger.setLevel(self.level)

    def stop(self) -> None:
        """Stop capturing logs."""
        logging.getLogger().removeHandler(self.handler)

    def get_logs(self, level: Optional[int] = None) -> List[str]:
        """Get captured log messages."""
        if level is None:
            return [record.getMessage() for record in self.logs]
        return [record.getMessage() for record in self.logs if record.levelno >= level]
