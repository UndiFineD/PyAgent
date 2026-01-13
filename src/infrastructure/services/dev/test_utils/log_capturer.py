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
from src.core.base.version import VERSION
from typing import Any, List, Optional
import logging

__version__ = VERSION

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