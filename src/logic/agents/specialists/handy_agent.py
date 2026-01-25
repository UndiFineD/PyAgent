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


"""Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.
"""

from __future__ import annotations

from pathlib import Path

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.local_context_recorder import \
    LocalContextRecorder
from src.logic.agents.specialists.mixins.handy_core_mixin import HandyCoreMixin
from src.logic.agents.specialists.mixins.handy_file_system_mixin import \
    HandyFileSystemMixin
from src.logic.agents.specialists.mixins.handy_terminal_mixin import \
    HandyTerminalMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class HandyAgent(BaseAgent, HandyFileSystemMixin, HandyTerminalMixin, HandyCoreMixin):
    """Provides a terminal-native interface for the agent to interact with the OS."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Handy Agent. "
            "Your role is to act as an 'Agentic Bash' – a terminal shell that understands codebase context. "
            "You provide tools for intelligent file search, system diagnosis, and command execution."
        )

        # Phase 108: Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    # Methods delegated to mixins
