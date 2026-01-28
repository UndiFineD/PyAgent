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

import collections.abc
import logging
import subprocess
import time
import types
from pathlib import Path
from typing import Any

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

import traceback
from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.common.models import CacheEntry, EventType, PromptTemplate, FailureClassification
from src.core.base.execution.shell_executor import ShellExecutor
from src.core.base.lifecycle.agent_core import BaseCore
from src.core.base.lifecycle.base_agent_core import BaseAgentCore
from src.core.base.lifecycle.version import VERSION
from src.core.base.mixins.governance_mixin import GovernanceMixin
# Import Mixins for Synaptic Modularization (Phase 317)
from src.core.base.mixins.identity_mixin import IdentityMixin
from src.core.base.mixins.knowledge_mixin import KnowledgeMixin
from src.core.base.mixins.multimodal_mixin import MultimodalMixin
from src.core.base.mixins.orchestration_mixin import OrchestrationMixin
from src.core.base.mixins.persistence_mixin import PersistenceMixin
from src.core.base.mixins.reflection_mixin import ReflectionMixin

# Advanced components (Lazy loaded or optional)
try:
    # pylint: disable=unused-import
    from src.infrastructure.swarm.orchestration.signals.signal_registry import \
        SignalRegistry
    from src.infrastructure.swarm.orchestration.system.tool_registry import \
        ToolRegistry
    from src.logic.agents.cognitive.long_term_memory import LongTermMemory
except (ImportError, ValueError):
    LongTermMemory = None
    SignalRegistry = None
    ToolRegistry = None

__version__ = VERSION


# pylint: disable=too-many-ancestors, too-many-instance-attributes
class BaseAgent(
    IdentityMixin,
    PersistenceMixin,
    KnowledgeMixin,
    OrchestrationMixin,
    GovernanceMixin,
    ReflectionMixin,
    MultimodalMixin,
):
    """
    Core AI Agent Shell (Synaptic modularization Phase 317).
    Inherits domain logic from specialized Mixins to maintain low complexity.
    """

    # Class-level attributes for shared state
    _prompt_templates: dict[str, PromptTemplate] = {}
    _response_cache: dict[str, CacheEntry] = {}
    _plugins: dict[str, Any] = {}
    _event_hooks: dict[EventType, list[collections.abc.Callable[[dict[str, Any]], None]]] = {}

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

    def __init__(self, file_path: str = ".", **kwargs: Any) -> None:
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
        MultimodalMixin.__init__(self, **kwargs)

        self._config = self.agent_logic_core.load_config_from_env()
        GovernanceMixin.__init__(self, config=self._config, **kwargs)

        # Post-init setup
        self._register_capabilities()
        self._token_usage = 0
        self._state_data: dict[str, Any] = {}
        self._post_processors: list[collections.abc.Callable[[str], str]] = []
        self._model: str | None = kwargs.get("model")
        self.recorder = kwargs.get("recorder")
        self.logger = logging.getLogger(self.__class__.__name__)
        self._system_prompt: str = "You are a helpful AI assistant."
        self.status_cache: dict[str, float] = {}

        # Context for task lineage
        self.context: CascadeContext | None = kwargs.get("context", None)

    def _run_command(self, cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
        """Run a shell command."""
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

        import asyncio  # pylint: disable=import-outside-toplevel

        try:
            # Check if there is an existing running event loop (Python 3.7+)
            try:
                asyncio.get_running_loop()
                # For compatibility in nested async
                result = "Async loop already running"
            except RuntimeError:
                # No running loop, safe to use asyncio.run
                result = asyncio.run(self.run_async(prompt))

            self._notify_webhooks("agent_complete", {"status": "success", "result": result})
            return result
        except RuntimeError as e:
            f_type = self._classify_exception(e)
            if hasattr(self, "context") and self.context:
                try:
                    self.context.log_failure(
                        stage=f"{self.__class__.__name__}.run",
                        error=str(e),
                        stack_trace=traceback.format_exc(),
                        failure_type=f_type
                    )
                except (RuntimeError, ValueError):
                    pass
            self._notify_webhooks("agent_error", {"error": str(e), "failure_type": f_type})
            return f"Error: {e} (Type: {f_type})"

    def _notify_webhooks(self, event: str, data: dict[str, Any]) -> None:
        """Helper to notify registered webhooks."""
        if not hasattr(self, "_webhooks") or not self._webhooks:
            return

        if not HAS_REQUESTS or requests is None:
            return

        # Resilience: Check status cache (TTL 15m)
        now = time.time()
        # Initialize if missing
        if not hasattr(self, "status_cache"):
            self.status_cache = {}

        payload = {"event": event, "data": data, "agent": self.agent_name}
        for url in self._webhooks:
            # Skip if recently failed (simple circuit breaker)
            if self.status_cache.get(url, 0) > now:
                continue

            try:
                requests.post(url, json=payload, timeout=5)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Backoff for 15 minutes on failure
                self.status_cache[url] = now + 900
                # pylint: disable=broad-exception-caught

    def _classify_exception(self, e: Exception) -> str:
        """
        Classify exception into FailureClassification enum.
        Phase 336: Standardized failure taxonomy implementation.
        """
        exc_str = str(e).lower()
        if isinstance(e, RecursionError) or "recursion" in exc_str:
            return FailureClassification.RECURSION_LIMIT.value
        if isinstance(e, MemoryError) or "memory" in exc_str:
            return FailureClassification.RESOURCE_EXHAUSTION.value
        if "connection" in exc_str or "timeout" in exc_str:
            return FailureClassification.NETWORK_FAILURE.value
        if "shard" in exc_str:
            return FailureClassification.SHARD_CORRUPTION.value
        if hasattr(FailureClassification, "AI_ERROR") and "hallucination" in exc_str:
            return FailureClassification.AI_ERROR.value

        return FailureClassification.UNKNOWN.value

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
        logging.info("[%s] Reasoning on prompt: %s...", self.__class__.__name__, prompt[:50])

        # 1. Governance & Quota Checks
        if hasattr(self, "_check_preemption"):
            await self._check_preemption()

        if hasattr(self, "quotas"):
            exceeded, reason = self.quotas.check_quotas()
            if exceeded:
                logging.error("Quota exceeded: %s", reason)
                return f"ERROR: {reason}"

        # 2. Prompt Construction
        # Combine system prompt, history, and current task
        sys_prompt = self._system_prompt
        # Inject multimodal instructions if mixin is present
        # (Check dynamically to avoid overwrite in __init__)
        if hasattr(self, "get_multimodal_instructions"):
            mm_instr = self.get_multimodal_instructions()
            if mm_instr not in sys_prompt:
                sys_prompt += f"\n\n{mm_instr}"

        full_prompt = f"SYSTEM: {sys_prompt}\n\n"
        if hasattr(self, "_build_prompt_with_history"):
            full_prompt += self._build_prompt_with_history(prompt)
        else:
            full_prompt += f"USER: {prompt}"

        # 3. Execution via Backend
        import asyncio  # pylint: disable=import-outside-toplevel

        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure.compute import backend as ab

            # Execute in thread to avoid blocking the async loop
            result = await asyncio.to_thread(
                ab.run_subagent,
                description=f"{self.__class__.__name__} core reasoning",
                prompt=full_prompt,
                original_content=self.current_content,
            )

            if result:
                # Update stats/usage
                if hasattr(self, "quotas"):
                    self.quotas.update_usage(len(full_prompt) // 4, len(result) // 4)
                return result
            return self._get_fallback_response()

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            f_type = self._classify_exception(e)
            logging.error("Think execution failed: %s (Type: %s)", e, f_type)

            # Telemetry Capture (Swarm Intelligence Fix)
            if self.context:
                try:
                    self.context.log_failure(
                        stage=f"{self.__class__.__name__}.think",
                        error=str(e),
                        stack_trace=traceback.format_exc(),
                        failure_type=f_type,
                        details={"prompt_preview": prompt[:100]}
                    )
                except Exception as telemetry_err:
                    logging.error(f"Failed to log failure to CascadeContext: {telemetry_err}")

            return f"Error encountered during agent reasoning: {str(e)} (Type: {f_type})"

    def get_model(self) -> str:
        """Get the current model name."""
        return self._model or "gemini-3-flash"

    def __enter__(self) -> BaseAgent:
        """Enter context."""
        try:
            # Check if there is an existing running event loop (Python 3.7+)
            try:
                asyncio.get_running_loop()
                # For compatibility in nested async
                result = "Async loop already running"
            except RuntimeError:
                # No running loop, safe to use asyncio.run
                result = asyncio.run(self.run_async(prompt))

            self._notify_webhooks("agent_complete", {"status": "success", "result": result})
            return result
        except RuntimeError as e:
            f_type = self._classify_exception(e)
            if hasattr(self, "context") and self.context:
                try:
                    self.context.log_failure(
                        stage=f"{self.__class__.__name__}.run",
                        error=str(e),
                        stack_trace=traceback.format_exc(),
                        failure_type=f_type
                    )
                except (RuntimeError, ValueError):
                    pass
            self._notify_webhooks("agent_error", {"error": str(e), "failure_type": f_type})
            return f"Error: {e} (Type: {f_type})"
                    import json  # pylint: disable=import-outside-toplevel

                    res_str = json.dumps(result)

                # Check for record_interaction or record
                if hasattr(self.recorder, "record_interaction"):
                    self.recorder.record_interaction(
                        provider=provider, model=model, prompt=prompt, result=res_str, meta=meta
                    )
                elif hasattr(self.recorder, "record"):
                    self.recorder.record(prompt, result)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.debug("BaseAgent: Failed to record interaction: %s", e)

    def verify_self(self, result: str) -> tuple[bool, str]:
        """Verify the integrity of a generated result."""
        return self.agent_logic_core.verify_self(result, 1.0)

    def _get_fallback_response(self) -> str:
        """Return a standardized fallback response."""
        return self.agent_logic_core.get_fallback_response()
