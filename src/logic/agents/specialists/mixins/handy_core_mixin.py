#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
HandyCoreMixin - Core recording and evaluation.
BRIEF SUMMARY
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE: Add HandyCoreMixin to a HandyAgent mixin stack to archive shell interactions via self.recorder and to expose a minimal terminal-oriented evaluation entrypoint; WHAT IT DOES: provides _record(tool_name, input_data, output) that attempts to archive interactions with metadata (phase/type/timestamp/tool) using self.recorder.record_interaction and a simple improve_content(prompt) that returns a static readiness string; WHAT IT SHOULD DO BETTER: emit richer, structured outputs, support async and transactional recorder usage, surface recorder errors for observability, make metadata configurable, and implement meaningful evaluation logic plus unit tests.

# FILE CONTENT SUMMARY: contains an Apache-2.0 header and short module docstring, imports time and typing (TYPE_CHECKING, Any), conditionally imports HandyAgent for typing, and defines class HandyCoreMixin with methods _record(self, tool_name, input_data, output) performing defensive recording when self.recorder is present and improve_content(self, prompt) returning "Handy Agent active. Ready for shell operations."# Licensed under the Apache License, Version 2.0 (the "License");"
from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent


class HandyCoreMixin:
""""Mixin for core recording and evaluation logic in HandyAgent.
    def _record(self: HandyAgent, tool_name: str, input_data: Any, output: str) -> None:
""""Archiving shell interaction for fleet intelligence.        if self."recorder:"            try:
                meta = {"phase": 108, "type": "shell", "timestamp": time.time(), "tool": tool_name}"                self.recorder.record_interaction("handy", "bash", str(input_data), output, meta=meta)"            except (AttributeError, RuntimeError, TypeError):
                pass

    def improve_content(self: HandyAgent, prompt: str) -> str:
""""Evaluates a terminal-oriented request.        _ = prompt  # "Mark as used"#         return "Handy Agent active. Ready for shell operations."