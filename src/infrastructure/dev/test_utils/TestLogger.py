#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .TestLogEntry import TestLogEntry
from contextlib import contextmanager
from typing import Any
from collections.abc import Iterator

__version__ = VERSION


class TestLogger:
    """Logger for test debugging.

    Captures logs during test execution for debugging.

    Example:
        logger=TestLogger()
        with logger.capture("test_name"):
            logger.info("Test started")
            # ... test code ...
        logs=logger.get_logs("test_name")
    """

    __test__ = False

    def __init__(self) -> None:
        """Initialize logger."""
        self._logs: dict[str, list[TestLogEntry]] = {}
        self._current_test: str | None = None

    def _log(self, level: str, message: str, **extra: Any) -> None:
        """Internal log method."""
        entry = TestLogEntry(
            level=level,
            message=message,
            test_name=self._current_test,
            extra=extra,
        )

        if self._current_test:
            if self._current_test not in self._logs:
                self._logs[self._current_test] = []
            self._logs[self._current_test].append(entry)

    def debug(self, message: str, **extra: Any) -> None:
        """Log debug message."""
        self._log("DEBUG", message, **extra)

    def info(self, message: str, **extra: Any) -> None:
        """Log info message."""
        self._log("INFO", message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        """Log warning message."""
        self._log("WARNING", message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        """Log error message."""
        self._log("ERROR", message, **extra)

    @contextmanager
    def capture(self, test_name: str) -> Iterator[TestLogger]:
        """Context manager to capture logs for a test.

        Args:
            test_name: Name of the test.

        Yields:
            Self for logging.
        """
        old_test = self._current_test
        self._current_test = test_name
        self._logs[test_name] = []
        try:
            yield self
        finally:
            self._current_test = old_test

    def get_logs(self, test_name: str) -> list[TestLogEntry]:
        """Get logs for a test."""
        return self._logs.get(test_name, [])

    def get_errors(self, test_name: str) -> list[TestLogEntry]:
        """Get error logs for a test."""
        return [entry for entry in self.get_logs(test_name) if entry.level == "ERROR"]

    def clear(self) -> None:
        """Clear all logs."""
        self._logs.clear()
