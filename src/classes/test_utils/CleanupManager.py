#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Callable, List

class CleanupManager:
    """Manages cleanup hooks for tests."""

    def __init__(self) -> None:
        """Initialize cleanup manager."""
        self.hooks: List[Callable[[], None]] = []

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
            except Exception:
                pass
