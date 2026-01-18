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

"""BaseAgent main class and core agent logic."""

from __future__ import annotations
from src.core.base.Version import VERSION
import subprocess
from pathlib import Path
from types import TracebackType
from typing import Any
from collections.abc import Callable
from src.core.base.models import (
    CacheEntry,
    EventType,
    PromptTemplate,
)
from src.core.base.AgentCore import BaseCore
from src.core.base.BaseAgentCore import BaseAgentCore
from src.core.base.ShellExecutor import ShellExecutor

# Import Mixins for Synaptic Modularization (Phase 317)
from src.core.base.mixins.IdentityMixin import IdentityMixin
from src.core.base.mixins.PersistenceMixin import PersistenceMixin
from src.core.base.mixins.KnowledgeMixin import KnowledgeMixin
from src.core.base.mixins.OrchestrationMixin import OrchestrationMixin
from src.core.base.mixins.GovernanceMixin import GovernanceMixin

# from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder # Moved to __init__

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

# Advanced components (Lazy loaded or optional)
try:
    from src.logic.agents.cognitive.LongTermMemory import LongTermMemory
    from src.infrastructure.orchestration.signals.SignalRegistry import SignalRegistry
    from src.infrastructure.orchestration.system.ToolRegistry import ToolRegistry
except (ImportError, ValueError):
    LongTermMemory = None
    SignalRegistry = None
    ToolRegistry = None

__version__ = VERSION

# Advanced components (Lazy loaded or optional)


class BaseAgent(
    IdentityMixin,
    PersistenceMixin,
    KnowledgeMixin,
    OrchestrationMixin,
    GovernanceMixin,
):
    """
    Core AI Agent Shell (Synaptic modularization Phase 317).
    Inherits domain logic from specialized Mixins to maintain low complexity.
    """

    # Class-level attributes for shared state
    _prompt_templates: dict[str, PromptTemplate] = {}
    _response_cache: dict[str, CacheEntry] = {}
    _plugins: dict[str, Any] = {}
    _event_hooks: dict[EventType, list[Callable[[dict[str, Any]], None]]] = {}

    def __init__(self, file_path: str, **kwargs: Any) -> None:
        """Initialize the BaseAgent with decentralized initialization."""
        self.file_path = Path(file_path)
        self._workspace_root = kwargs.get("repo_root") or BaseCore.detect_workspace_root(self.file_path)
        self.agent_logic_core = BaseAgentCore()
        self.core = BaseCore(workspace_root=self._workspace_root)

        self.previous_content = ""
        self.current_content = ""

        # Decentralized Mixin Initialization
        IdentityMixin.__init__(self, **kwargs)
        PersistenceMixin.__init__(self, **kwargs)
        KnowledgeMixin.__init__(
            self,
            agent_name=self.agent_name,
            workspace_root=Path(self._workspace_root),
            **kwargs,
        )
        OrchestrationMixin.__init__(self, **kwargs)

        self._config = self.agent_logic_core.load_config_from_env()
        GovernanceMixin.__init__( self, config=self._config, **kwargs)

        # Post-init setup
        self._register_capabilities()
        self._token_usage = 0
        self._state_data: dict[str, Any] = {}
        self._post_processors: list[Callable[[str], str]] = []
        self._model: str | None = kwargs.get("model")
        self._system_prompt: str = "You are a helpful AI assistant."

    def _run_command(
        self, cmd: list[str], timeout: int = 120
    ) -> subprocess.CompletedProcess[str]:
        return ShellExecutor.run_command(
            cmd, self._workspace_root, self.agent_name, timeout=timeout
        )

    async def run(self, prompt: str) -> str:
        """Main execution entry point."""
        self.previous_content = self.current_content
        result = await self.think(prompt)
        self.current_content = result
        return result

    def get_model(self) -> str:
        return self._model or "gemini-3-flash"

    def __enter__(self) -> BaseAgent:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def calculate_anchoring_strength(self, result: str) -> float:
        return self.agent_logic_core.calculate_anchoring_strength(
            result, getattr(self, "context_pool", {})
        )

    def verify_self(self, result: str) -> tuple[bool, str]:
        return self.agent_logic_core.verify_self(result)

    def _get_fallback_response(self) -> str:
        return self.agent_logic_core.get_fallback_response()

