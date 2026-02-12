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
Base Agent Interface - Principal PyAgent Abstract Base

Principal agent interface for PyAgent, supporting mixin-based architecture.
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Subclassed by specialized agents (e.g., CoderAgent, ResearchAgent) to provide core orchestration,
state management, and tool-use capabilities.

WHAT IT DOES:
The BaseAgent class provides the foundational logic for all agents in the swarm, including:
1. Mixin Integration: Seamlessly blends capabilities from identity, status, and messaging mixins.
2. Async Execution: Core loop supporting concurrent I/O, network requests, and tool execution.
3. State Orchestration: Manages agent health, focus, and memory transitions.
4. Tool Utilization: Interfaces with internal and external tools via a standardized dispatch mechanism.
5. Error Resilience: Implements robust exception handling and state recovery patterns.

WHAT IT SHOULD DO BETTER:
- Further decoupling of specialized logic into standalone mixins to prevent class bloat.
- Implementation of more granular tracing for complex multi-agent execution spans.
- Optimization of state serialization for high-frequency environment updates.
"""

from __future__ import annotations

import asyncio
import collections.abc
import logging
import subprocess
import time
import traceback
from pathlib import Path
from typing import Any

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.common.models import CacheEntry, EventType, PromptTemplate, FailureClassification
from src.core.base.execution.shell_executor import ShellExecutor
from src.core.base.lifecycle.agent_core import BaseCore
from src.core.base.lifecycle.base_agent_core import BaseAgentCore
from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.logic_manifest import LogicManifest
from src.core.base.lifecycle.skill_manager import SkillManager
from src.infrastructure.security.audit.scam_detector import ScamDetector
from src.core.base.mixins.governance_mixin import GovernanceMixin
# Import Mixins for Synaptic Modularization (Phase 317)
from src.core.base.mixins.environment_mixin import EnvironmentMixin
from src.core.base.mixins.identity_mixin import IdentityMixin
from src.core.base.mixins.rl_optimization_mixin import RLOptimizationMixin
from src.core.base.mixins.knowledge_mixin import KnowledgeMixin
from src.core.base.mixins.multimodal_mixin import MultimodalMixin
from src.core.base.mixins.orchestration_mixin import OrchestrationMixin
from src.core.base.mixins.persistence_mixin import PersistenceMixin
from src.core.base.mixins.reflection_mixin import ReflectionMixin
from src.core.base.mixins.security_mixin import SecurityMixin
from src.core.base.mixins.task_queue_mixin import TaskQueueMixin
from src.core.base.mixins.stream_manager_mixin import StreamManagerMixin
from src.core.base.mixins.task_manager_mixin import TaskManagerMixin
from src.core.base.mixins.tool_framework_mixin import ToolFrameworkMixin
from src.core.base.mixins.prompt_loader_mixin import PromptLoaderMixin
from src.core.base.mixins.streaming_mixin import StreamingMixin

# Cognitive Cores
from src.core.memory.automem_core import AutoMemCore
from src.core.reasoning.cort_core import CoRTReasoningCore as CoRTCore

logger = logging.getLogger(__name__)

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

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
    RLOptimizationMixin,  # Phase 321
    PersistenceMixin,
    KnowledgeMixin,
    OrchestrationMixin,
    GovernanceMixin,
    ReflectionMixin,
    MultimodalMixin,
    SecurityMixin,
    TaskQueueMixin,
    StreamManagerMixin,
    TaskManagerMixin,
    ToolFrameworkMixin,
    EnvironmentMixin,
    PromptLoaderMixin,
    StreamingMixin,
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
        # Extract arguments consumed by BaseAgent to prevent leaking them to object.__init__
        inference_engine = kwargs.pop("inference_engine", "gemini-3-flash")
        manifest_data = kwargs.pop("manifest", {})
        repo_root = kwargs.pop("repo_root", None)
        memory_config = kwargs.pop("memory_config", {})

        super().__init__(**kwargs)  # Phase 317: Ensure all mixins are initialized
        
        self.file_path = Path(file_path)
        self._workspace_root = repo_root or BaseCore.detect_workspace_root(self.file_path)
        self.agent_logic_core = BaseAgentCore()
        self.core = BaseCore(workspace_root=self._workspace_root)

        # Swarm Singularity: Initialize Logic Shard and Skill Manager
        self.manifest = LogicManifest.from_dict(manifest_data)
        self.skill_manager = SkillManager(self)
        self.scam_detector = ScamDetector()

        # Initialize Cognitive Core Components
        if isinstance(memory_config, dict) and "workspace_root" not in memory_config:
            memory_config["workspace_root"] = str(self._workspace_root)
        self.memory_core = AutoMemCore(config=memory_config)
        
        # Determine inference engine (handle string vs object)
        from src.inference.engine import InferenceEngine
        if isinstance(inference_engine, str):
            self.inference_engine = InferenceEngine(model_name=inference_engine)
        else:
            self.inference_engine = inference_engine
            
        self.reasoning_core = CoRTCore(inference_engine=self.inference_engine)

        self.previous_content = ""
        self.current_content = ""

        # Decentralized Mixin Initialization
        # Restore popped kwargs for manual mixin initialization if needed
        full_kwargs = kwargs.copy()
        full_kwargs.update({
            "inference_engine": inference_engine, 
            "manifest": manifest_data,
            "repo_root": repo_root,
            "memory_config": memory_config
        })

        IdentityMixin.__init__(self, **full_kwargs)
        PersistenceMixin.__init__(self, **full_kwargs)
        KnowledgeMixin.__init__(
            self,
            agent_name=self.manifest.role,
            workspace_root=Path(self._workspace_root),
            **full_kwargs,
        )
        OrchestrationMixin.__init__(self, **full_kwargs)
        ReflectionMixin.__init__(self, **full_kwargs)
        MultimodalMixin.__init__(self, **full_kwargs)
        SecurityMixin.__init__(self, **full_kwargs)
        TaskQueueMixin.__init__(self, **full_kwargs)
        StreamManagerMixin.__init__(self, **kwargs)
        TaskManagerMixin.__init__(self, **kwargs)
        ToolFrameworkMixin.__init__(self, **kwargs)
        PromptLoaderMixin.__init__(self, **kwargs)
        StreamingMixin.__init__(self, **kwargs)

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

        # Load system prompt from file if available, otherwise use default
        self._system_prompt: str = self._load_system_prompt()

        self.status_cache: dict[str, float] = {}

        # Context for task lineage
        self.context: CascadeContext | None = kwargs.get("context", None)

    async def setup(self) -> None:
        """Asynchronous setup for the Universal Agent shell."""
        logger.info("Initializing Universal Agent [%s]", self.manifest.role)

        # Load skills defined in logic manifest
        for skill_name in self.manifest.required_skills:
            await self.skill_manager.load_skill(skill_name)

        # Register capabilities from loaded skills
        self._register_capabilities()

    async def run_task(self, task_manifest: dict[str, Any]) -> Any:
        """
        Executes a task based on a Logic Manifest.
        This is the entry point for the Universal Agent's cognitive loop.
        """
        start_time = time.time()
        # Load any task-specific skills dynamically
        required_skills = task_manifest.get("required_skills", [])
        for skill in required_skills:
            await self.skill_manager.load_skill(skill)

        # Execute reasoning phase
        context = task_manifest.get("context", "")

        # Phase 321: RL-Guided Cognitive Loop
        best_action = self.get_best_action(context)
        if best_action:
            logger.info("RLOptimization: Using learned policy for state: %s", context[:50])
            # Implementation can expand to use best_action to guide ReasoningCore

        plan = await self.reasoning_core.reason(context)

        # Dispatch to appropriate skills
        logger.info("Universal Agent executing plan: %s", plan)

        # Swarm Singularity: Peer Audit (if requested)
        if task_manifest.get("audit", False):
            safe = await self.scam_detector.audit_response(context, str(plan), [])
            if not safe:
                logger.danger("Audit failed: Hallucination or Scam detected!")
                # Record negative reward
                self.record_step(action="reason", reward=-1.0, next_state="blocked", done=True)
                return {"status": "blocked", "reason": "audit_failed"}

        # Success! Record positive reward indexed by latency
        latency = time.time() - start_time
        reward = max(0.0, 1.0 - (latency / 10.0))  # Reward based on speed, min 0
        self.record_step(action="reason", reward=reward, next_state="success", done=True)

        return {"status": "success", "agent_mode": self.manifest.role, "result": plan}

    async def initialize_persona(self) -> None:
        """Asynchronously load the system prompt and initialize cognitive context."""
        # Using PromptLoaderMixin to load the persona from the library
        agent_type = getattr(self, "agent_type", "base")
        self._system_prompt = await self.load_prompt(agent_type, "system")

        # Link to reasoning and memory
        if hasattr(self, "memory_core"):
            await self.memory_core.record_event("persona_loaded", {"agent_type": agent_type})

    def _load_system_prompt(self) -> str:
        """Load system prompt from file if available, otherwise use class-defined or minimal fallback."""
        try:
            # Primary: Try to load from data/agents/{agent_name}/prompt.txt
            prompt_file = Path(self._workspace_root) / "data" / "agents" / self.agent_name / "prompt.txt"
            if prompt_file.exists():
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        if hasattr(self, 'logger') and self.logger:
                            self.logger.info(f"Loaded system prompt from {prompt_file}")
                        return content

            # Secondary: Check if class has a _system_prompt attribute (agent-specific fallback)
            class_prompt = getattr(self.__class__, '_system_prompt', None)
            if class_prompt and class_prompt != "You are an AI.":
                if hasattr(self, 'logger') and self.logger:
                    self.logger.info(f"Using class-defined system prompt for {self.agent_name}")
                return class_prompt

        except (OSError, ValueError, UnicodeError) as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.warning(
                    f"[Robustness] Failed to load system prompt for {self.agent_name}: {e}",
                    exc_info=True
                )
        except Exception:  # pylint: disable=broad-exception-caught
            # Unexpected error: log and re-raise to avoid masking bugs
            if hasattr(self, 'logger') and self.logger:
                self.logger.exception(f"[Robustness] Unexpected error loading system prompt for {self.agent_name}")
            raise

        # Tertiary: Minimal fallback prompt
        return "You are an AI."

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

        # import asyncio  # pylint: disable=import-outside-toplevel

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
            except requests.RequestException as e:
                # Backoff for 15 minutes on failure (network/requests specific)
                self.status_cache[url] = now + 900
                logging.warning(f"[Robustness] Failed to notify webhook {url}: {e}", exc_info=True)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Unexpected errors should be logged fully but not mask other bugs
                logging.exception(f"[Robustness] Unexpected error while notifying webhook {url}: {e}")

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
        # import asyncio  # pylint: disable=import-outside-toplevel

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

        except (ImportError, RuntimeError, OSError, ValueError, TypeError) as e:
            f_type = self._classify_exception(e)
            logging.error("[Robustness] Think execution failed: %s (Type: %s)", e, f_type, exc_info=True)

            # Telemetry Capture (Swarm Intelligence Fix)
            if getattr(self, "context", None):
                try:
                    getattr(self, "context").log_failure(
                        stage=f"{self.__class__.__name__}.think",
                        error=str(e),
                        stack_trace=traceback.format_exc(),
                        failure_type=f_type,
                        details={"prompt_preview": prompt[:100]}
                    )
                except (RuntimeError, ValueError, TypeError, OSError) as telemetry_err:
                    logging.error(
                        f"[Robustness] Failed to log failure to CascadeContext: {telemetry_err}",
                        exc_info=True
                    )

            return f"Error encountered during agent reasoning: {str(e)} (Type: {f_type})"
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            logging.exception("[Robustness] Unexpected error in think execution, re-raising")
            raise

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
                result = asyncio.run(self.run_async(self._system_prompt))

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
                provider="unknown", model=self._model, prompt=self._system_prompt, result=res_str, meta={}
            )
        elif hasattr(self.recorder, "record"):

            try:
                self.recorder.record(self._system_prompt, result)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.debug("[Robustness] BaseAgent: Failed to record interaction: %s", e, exc_info=True)

    def verify_self(self, result: str) -> tuple[bool, str]:
        """Verify the integrity of a generated result."""
        return self.agent_logic_core.verify_self(result, 1.0)

    def _get_fallback_response(self) -> str:
        """Return a standardized fallback response."""
        return self.agent_logic_core.get_fallback_response()
