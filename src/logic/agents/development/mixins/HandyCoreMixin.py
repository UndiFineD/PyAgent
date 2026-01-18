# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.development.HandyAgent import HandyAgent

class HandyCoreMixin:
    """Mixin for core recording and evaluation logic in HandyAgent."""

    def _record(self: HandyAgent, tool_name: str, input: Any, output: str) -> None:
        """Archiving shell interaction for fleet intelligence."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "shell", "timestamp": time.time()}
                self.recorder.record_interaction(
                    "handy", "bash", str(input), output, meta=meta
                )
            except Exception:
                pass

    def improve_content(self: HandyAgent, prompt: str) -> str:
        """Evaluates a terminal-oriented request."""
        return "Handy Agent active. Ready for shell operations."
