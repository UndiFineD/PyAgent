
"""
Handy core mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent


class HandyCoreMixin:
    """Mixin for core recording and evaluation logic in HandyAgent."""

    def _record(self: HandyAgent, tool_name: str, input_data: Any, output: str) -> None:
        """Archiving shell interaction for fleet intelligence."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "shell", "timestamp": time.time(), "tool": tool_name}
                self.recorder.record_interaction("handy", "bash", str(input_data), output, meta=meta)
            except (AttributeError, RuntimeError, TypeError):
                pass

    def improve_content(self: HandyAgent, prompt: str) -> str:
        """Evaluates a terminal-oriented request."""
        _ = prompt  # Mark as used
        return "Handy Agent active. Ready for shell operations."
