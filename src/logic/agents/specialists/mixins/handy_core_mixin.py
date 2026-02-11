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

"""
Handy core mixin.py module.
"""
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
