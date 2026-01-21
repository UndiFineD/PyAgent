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
from src.core.base.lifecycle.version import VERSION
import subprocess
import logging
from pathlib import Path
from types import TracebackType
from typing import Any
from collections.abc import Callable
from src.core.base.common.models import (
    CacheEntry,
    EventType,
    PromptTemplate,
)
from src.core.base.lifecycle.agent_core import BaseCore
from src.core.base.lifecycle.base_agent_core import BaseAgentCore
from src.core.base.execution.shell_executor import ShellExecutor

# Import Mixins for Synaptic Modularization (Phase 317)
from src.core.base.mixins.identity_mixin import IdentityMixin
from src.core.base.mixins.persistence_mixin import PersistenceMixin
from src.core.base.mixins.knowledge_mixin import KnowledgeMixin
from src.core.base.mixins.orchestration_mixin import OrchestrationMixin
from src.core.base.mixins.governance_mixin import GovernanceMixin
from src.core.base.mixins.reflection_mixin import ReflectionMixin

# from src.infrastructure.compute.backend.LocalContextRecorder import LocalContextRecorder # Moved to __init__

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

# Advanced components (Lazy loaded or optional)
try:
    from src.logic.agents.cognitive.long_term_memory import LongTermMemory
    from src.infrastructure.swarm.orchestration.signals.signal_registry import SignalRegistry
    from src.infrastructure.swarm.orchestration.system.tool_registry import ToolRegistry
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
    ReflectionMixin,
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

    @classmethod
    def register_plugin(cls, name_or_plugin: Any, plugin: Any | None = None) -> None:
        """Register a plugin with the agent."""
        if plugin is None:
            # Called with one arg: register_plugin(plugin)
            plugin_obj = name_or_plugin
            name = getattr(plugin_obj, "name", "unknown")
        else:
            # Called with two args: register_plugin(name, plugin)
            name = name_or_plugin
            plugin_obj = plugin
        cls._plugins[name] = plugin_obj

    @classmethod
    def unregister_plugin(cls, name: str) -> bool:
        """Unregister a plugin."""
        if name in cls._plugins:
            del cls._plugins[name]
            return True
        return False

    @classmethod
    def get_plugin(cls, name: str) -> Any:
        """Get a registered plugin."""
        return cls._plugins.get(name)

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
        ReflectionMixin.__init__(self, **kwargs)

        self._config = self.agent_logic_core.load_config_from_env()
        GovernanceMixin.__init__( self, config=self._config, **kwargs)

        # Post-init setup
        self._register_capabilities()
        self._token_usage = 0
        self._state_data: dict[str, Any] = {}
        self._post_processors: list[Callable[[str], str]] = []
        self._model: str | None = kwargs.get("model")
        self.recorder = kwargs.get("recorder")
        self.logger = logging.getLogger(self.__class__.__name__)
        self._system_prompt: str = "You are a helpful AI assistant."

    def _run_command(
        self, cmd: list[str], timeout: int = 120
    ) -> subprocess.CompletedProcess[str]:
        return ShellExecutor.run_command(
            cmd,
            self._workspace_root,
            self.agent_name,
            models_config=getattr(self, "models", None),
            timeout=timeout,
        )

    def run(self, prompt: str | None = None) -> str:
        """
        Synchronous execution entry point for legacy support.
        """
        if prompt is None:
            # Default behavior for no prompt (usually legacy loop)
            # In Phase 5/6, this triggers an 'agent_complete' event
            self._notify_webhooks("agent_complete", {"status": "success"})
            return "No prompt provided."
            
        import asyncio
        try:
            # Check if there is an existing event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                # For compatibility in nested async
                result = "Async loop already running"
            else:
                result = asyncio.run(self.run_async(prompt))
                
            self._notify_webhooks("agent_complete", {"status": "success", "result": result})
            return result
        except Exception as e:
            self._notify_webhooks("agent_error", {"error": str(e)})
            return f"Error: {e}"

    def _notify_webhooks(self, event: str, data: dict[str, Any]) -> None:
        """Helper to notify registered webhooks."""
        if not hasattr(self, "_webhooks") or not self._webhooks:
            return
            
        if not HAS_REQUESTS or requests is None:
            return
            
        payload = {"event": event, "data": data, "agent": self.agent_name}
        for url in self._webhooks:
            try:
                requests.post(url, json=payload, timeout=5)
            except Exception:
                pass

    async def run_async(self, prompt: str) -> str:
        """Main execution entry point (formerly run)."""
        self.previous_content = self.current_content
        
        # Reset reflection state for new task
        self.reset_reflection()
        
        result = await self.think(prompt)
        
        # Autonomous Self-Reflection (Phase 320)
        result = await self.reflect(prompt, result)
        
        self.current_content = result
        return result

    async def think(self, prompt: str) -> str:
        """
        The core synaptic processing method.
        Decomposes the prompt, consults knowledge, and produces a reasoning-based response.
        """
        import logging
        logging.info(f"[{self.__class__.__name__}] Reasoning on prompt: {prompt[:50]}...")

        # 1. Governance & Quota Checks
        if hasattr(self, "_check_preemption"):
            await self._check_preemption()
        
        if hasattr(self, "quotas"):
            exceeded, reason = self.quotas.check_quotas()
            if exceeded:
                logging.error(f"Quota exceeded: {reason}")
                return f"ERROR: {reason}"

        # 2. Prompt Construction
        # Combine system prompt, history, and current task
        full_prompt = f"SYSTEM: {self._system_prompt}\n\n"
        if hasattr(self, "_build_prompt_with_history"):
            full_prompt += self._build_prompt_with_history(prompt)
        else:
            full_prompt += f"USER: {prompt}"

        # 3. Execution via Backend
        import asyncio
        try:
            from src.infrastructure import backend as ab
            
            # Execute in thread to avoid blocking the async loop if the backend is sync
            result = await asyncio.to_thread(
                ab.run_subagent, 
                description=f"{self.__class__.__name__} core reasoning",
                prompt=full_prompt,
                original_content=self.current_content
            )
            
            if result:
                # Update stats/usage
                if hasattr(self, "quotas"):
                    self.quotas.update_usage(len(full_prompt) // 4, len(result) // 4)
                return result
            
            return self._get_fallback_response()
            
        except Exception as e:
            logging.error(f"Think execution failed: {e}")
            return f"Error encountered during agent reasoning: {str(e)}"

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

    def _record(
        self,
        prompt: str,
        result: str,
        provider: str = "Internal",
        model: str = "AgentLogic",
        meta: dict[str, Any] | None = None,
    ) -> None:
        """Helper to record diagnostic or telemetry events to the fleet recorder."""
        if hasattr(self, "recorder") and self.recorder:
            try:
                if isinstance(result, (dict, list)):
                    from json import dumps
                    result = dumps(result)
                
                # Check for record_interaction or record
                if hasattr(self.recorder, "record_interaction"):
                    self.recorder.record_interaction(
                        provider=provider,
                        model=model,
                        prompt=prompt,
                        result=result,
                        meta=meta
                    )
                elif hasattr(self.recorder, "record"):
                    self.recorder.record(prompt, result)
            except Exception as e:
                import logging
                logging.debug(f"BaseAgent: Failed to record interaction: {e}")

    def verify_self(self, result: str) -> tuple[bool, str]:
        return self.agent_logic_core.verify_self(result, 1.0)

    def _get_fallback_response(self) -> str:
        return self.agent_logic_core.get_fallback_response()

