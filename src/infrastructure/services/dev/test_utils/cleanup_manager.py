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


"""Auto-extracted class from agent_test_utils.py
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CleanupManager:
    """Manages cleanup hooks for tests."""

    def __init__(self) -> None:
        """Initialize cleanup manager."""
        self.hooks: list[Callable[[], None]] = []

    def add_hook(self, hook: Callable[[], None]) -> None:
        """Add cleanup hook."""
        self.hooks.append(hook)

    def register(self, hook: Callable[[], None]) -> None:
        """Compatibility alias for add_hook."""
        self.add_hook(hook)

    def cleanup(self) -> None:
        """Execute all cleanup hooks."""
        for hook in reversed(self.hooks):
            try:
                hook()
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                logging.debug("Cleanup hook execution failed.")
