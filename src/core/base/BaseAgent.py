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
from src.core.base.version import VERSION
from src.core.base.utilities import as_tool
from src.core.base.exceptions import CycleInterrupt
import logging
import asyncio
import subprocess
import sys
import time
from pathlib import Path
from types import TracebackType
from typing import Any
from collections.abc import Callable
from src.core.base.models import (
    AgentConfig,
    AgentState,
    CacheEntry,
    ConversationMessage,
    EventHook,
    EventType,
    HealthCheckResult,
    MessageRole,
    PromptTemplate,
    ResponseQuality,
    AgentPriority,
)
from src.core.base.AgentCore import BaseCore
from src.core.base.BaseAgentCore import BaseAgentCore
from src.core.base.registry import AgentRegistry
from src.core.base.ShardedKnowledgeCore import ShardedKnowledgeCore
from src.core.base.state import AgentStateManager
from src.core.base.delegation import AgentDelegator
from src.core.base.shell import ShellExecutor
from src.core.base.scratchpad import AgentScratchpad
from src.core.base.history import AgentConversationHistory
# from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder # Moved to __init__
from src.core.base.managers.ResourceQuotaManager import ResourceQuotaManager, QuotaConfig

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

# Advanced components (Lazy loaded or optional)
try:
    from src.logic.agents.cognitive.LongTermMemory import LongTermMemory
    from src.infrastructure.orchestration.SignalRegistry import SignalRegistry
    from src.infrastructure.orchestration.ToolRegistry import ToolRegistry
except (ImportError, ValueError):
    LongTermMemory = None
    SignalRegistry = None
    ToolRegistry = None

__version__ = VERSION

# Advanced components (Lazy loaded or optional)







class BaseAgent:
    """Shell class for AI-powered agents. Logic delegated to BaseAgentCore."""

    # Class-level attributes for shared state
    _prompt_templates: dict[str, PromptTemplate] = {}
    _response_cache: dict[str, CacheEntry] = {}
    _plugins: dict[str, Any] = {}
    _event_hooks: dict[EventType, list[Callable[[dict[str, Any]], None]]] = {}

    def __init__(self, file_path: str, **kwargs: Any) -> None:
        """Initialize the BaseAgent with file path.

        Args:
            file_path: Path to the file to improve. Can be absolute or relative.
                        Will be converted to pathlib.Path object.
            **kwargs: Additional arguments for backward compatibility/testing.
                      Supported: repo_root, dry_run
        """
        self.file_path = Path(file_path)

        # Handle repo_root override (useful for tests)
        if "repo_root" in kwargs:
            self._workspace_root = kwargs["repo_root"]
        else:
            self._workspace_root = BaseCore.detect_workspace_root(self.file_path)

        # Handle dry_run in config if passed
        self._dry_run_init = kwargs.get("dry_run", False)

        self.agent_logic_core = BaseAgentCore()  # Pure logic core (Rust-convertible)
        self.core = BaseCore(workspace_root=self._workspace_root)

        self.previous_content: str = ""
        self.current_content: str = ""
        self.fleet: Any = None  # FleetManager reference
        self.capabilities: list[str] = ["base"]  # Phase 241: Default capabilities

        # Phase 260: Priority and Preemption
        self.priority: AgentPriority = AgentPriority.NORMAL
        self._suspended: bool = False

        # Knowledge Trinity initialization (Phase 126)
        try:
            from src.core.knowledge.knowledge_engine import KnowledgeEngine
            agent_name = self.__class__.__name__.lower().replace("agent", "") or "base"
            self.knowledge = KnowledgeEngine(agent_id=agent_name, base_path=Path("data/agents"))
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None

        # Phase 241: Auto-register capabilities if SignalRegistry is available
        self._register_capabilities()

        # Strategy for agent execution (Phase 130: Lazy-loaded to avoid core-on-logic dependency)
        self._strategy: Any | None = None

        # New attributes for enhanced functionality
        self._state: AgentState = AgentState.INITIALIZED
        self._history_manager = AgentConversationHistory()
        self._scratchpad_manager = AgentScratchpad()
        self._config: AgentConfig = self._load_config()
        self._token_usage = 0
        self._state_data: dict[str, Any] = {}
        self._post_processors: list[Callable[[str], str]] = []
        self._model: str | None = None
        self._is_stop_requested = False
        self._system_prompt: str = "You are a helpful AI assistant."

        # Phase 245: RESOURCE QUOTAS & BUDGETS
        self.quotas = ResourceQuotaManager(
            config=QuotaConfig(
                max_tokens=getattr(self._config, 'max_tokens_per_session', None),
                max_time_seconds=getattr(self._config, 'max_time_per_session', None)
            )
        )

        self._local_global_context = None

        # Advanced features
        # Derive agent name for data isolation (e.g., CoderAgent -> "coder")
        self.agent_name = self.__class__.__name__.lower().replace("agent", "") or "base"
        self.memory: LongTermMemory | None = LongTermMemory(agent_name=self.agent_name) if LongTermMemory else None

        # Phase 143: Sharded Knowledge initialization
        self.sharded_knowledge = ShardedKnowledgeCore(base_path=Path("data/agents"))

        self.registry: SignalRegistry | None = SignalRegistry() if SignalRegistry else None
        self.tool_registry: ToolRegistry | None = ToolRegistry() if ToolRegistry else None

        # Intelligence Harvesting (Phase 108)
        from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
        self.recorder = LocalContextRecorder(Path(self._workspace_root), f"{self.__class__.__name__}_Agent")

    def _register_capabilities(self) -> None:
        """Emits a signal with agent capabilities for discovery."""
        try:
            import asyncio
            from src.infrastructure.orchestration.SignalRegistry import SignalRegistry
            signals = SignalRegistry()

            payload = self.agent_logic_core.prepare_capability_payload(
                self.__class__.__name__,
                self.get_capabilities()
            )

            # Schedule the async emit to run in the background
            try:
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                if loop.is_running():
                    asyncio.create_task(signals.emit("agent_capability_registration", payload))
                else:
                    loop.run_until_complete(signals.emit("agent_capability_registration", payload))
            except Exception:
                pass
        except Exception:
            pass

    def suspend(self) -> None:
        self._suspended = True

    def resume(self) -> None:
        self._suspended = False

    def log_distributed(self, level: str, message: str, **kwargs) -> None:
        """Publishes a log to the distributed logging system."""
        if hasattr(self, "fleet") and self.fleet:
            logging_agent = self.fleet.agents.get("Logging")
            if logging_agent:
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(logging_agent.broadcast_log(level, self.__class__.__name__, message, kwargs))
                except RuntimeError:
                    asyncio.run(logging_agent.broadcast_log(level, self.__class__.__name__, message, kwargs))

    async def _check_preemption(self) -> None:
        while self._suspended:
            await asyncio.sleep(0.5)

    def get_capabilities(self) -> list[str]:
        return self.capabilities

    @property
    def strategy(self) -> Any:
        if not hasattr(self, "_strategy") or self._strategy is None:
            try:
                from src.logic.strategies.DirectStrategy import DirectStrategy
                self._strategy = DirectStrategy()
            except (ImportError, ModuleNotFoundError):
                self._strategy = None
        return self._strategy

    @classmethod
    def from_config_file(cls, config_path: Path) -> BaseAgent:
        """Create an agent instance from a configuration file.

        Args:
            config_path: Path to the JSON configuration file.

        Returns:
            Initialized Agent.
        """
        import json
        try:
            config = json.loads(Path(config_path).read_text())
            repo_root = config.get("repo_root", None)
            # file_path is mandatory, assuming the config file itself acts as the 'file' or config specifies it
            # Attempt to derive file_path from config, or use config_path as dummy
            file_path = config.get("file_path", str(config_path))
            return cls(file_path, repo_root=repo_root)
        except Exception as e:
            logging.error(f"Failed to load agent from config {config_path}: {e}")
            raise

    @strategy.setter
    def strategy(self, value: Any) -> None:
        self._strategy = value

    def _run_command(self, cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
        models_config = getattr(self, 'models', None)
        return ShellExecutor.run_command(cmd, self._workspace_root, self.agent_name, models_config=models_config, timeout=timeout)

    @property
    def global_context(self) -> Any:
        if hasattr(self, 'fleet') and self.fleet and hasattr(self.fleet, 'global_context'):
            return self.fleet.global_context
        if self._local_global_context is None:
            try:
                from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine
                self._local_global_context = GlobalContextEngine(self._workspace_root)
            except (ImportError, ValueError): pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        self._local_global_context = value

    def register_tools(self, registry: ToolRegistry) -> None:
        if not registry: return
        for method, cat, prio in self.agent_logic_core.collect_tools(self):
            # Fix: Correct order is (owner_name, func, category, priority)
            registry.register_tool(self.__class__.__name__, method, cat, prio)

    def calculate_anchoring_strength(self, result: str) -> float:
        return self.agent_logic_core.calculate_anchoring_strength(result, getattr(self, 'context_pool', {}))

    def verify_self(self, result: str) -> tuple[bool, str]:
        return self.agent_logic_core.verify_self(result)

    def _load_config(self) -> AgentConfig:
        return self.agent_logic_core.load_config_from_env()

    def set_strategy(self, strategy: Any) -> None:
        self.strategy = strategy
        logging.info(self.agent_logic_core.set_strategy(strategy))

    @property
    def state(self) -> AgentState:
        return self._state

    def set_model(self, model: str) -> None:
        self._model = model
        logging.debug(f"Model set to: {model}")

    def _track_tokens(self, input_tokens: int, output_tokens: int) -> None:
        self._last_token_usage = self.agent_logic_core.process_token_tracking(
            input_tokens, output_tokens, self.get_model() or "gpt-4o"
        )

    def get_model(self) -> str | None:
        return self._model or self._config.model or None

    def __enter__(self) -> BaseAgent:
        AgentRegistry().register(self)
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> bool:
        AgentRegistry().unregister(self.agent_name)
        if exc_type is not None:
            self._state = AgentState.ERROR
            self._trigger_event(EventType.ERROR, {"exception": exc_val})
        else:
            self._state = AgentState.COMPLETED
        return False

    def stop(self) -> None:
        """Request the agent to stop its current operation."""
        logging.info(f"Stop requested for {self.__class__.__name__}")
        self._is_stop_requested = True

    def register_webhook(self, url: str) -> None:
        """Registers a webhook URL for notifications."""
        if not hasattr(self, '_webhooks'):
            self._webhooks: list[Any] = []
        if url not in self._webhooks:
            self._webhooks.append(url)

    def run(self, prompt: str = "") -> None:
        self._is_stop_requested = False
        try:
            import asyncio
            coro = self.improve_content(prompt)

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                # If loop is already running, we can't block.
                # Use a task but we won't wait for it here, which is better than just a warning
                # but still not ideal for a sync 'run' method.
                asyncio.create_task(coro)
            else:
                loop.run_until_complete(coro)

            if not self._is_stop_requested: self.update_file()
            webhooks = getattr(self, '_webhooks', [])
            for url in webhooks:
                if HAS_REQUESTS and requests:
                    requests.post(url, json={"event": "agent_complete", "status": "success", "file": str(self.file_path), "timestamp": time.time()}, timeout=5)
        except Exception as e:
            logging.error(f"Error running {self.__class__.__name__}: {e}")
            raise

    def read_previous_content(self) -> str:
        """Read existing file content."""
        self._state = AgentState.READING
        self._trigger_event(EventType.PRE_READ, {"file_path": str(self.file_path)})

        try:
            if self.file_path.is_file():
                self.previous_content = self.file_path.read_text(encoding='utf-8')
            else:
                logging.warning(f"File not found: {self.file_path}. Using default content.")
                self.previous_content = self._get_default_content()
        except Exception as e:
            logging.error(f"Failed to read file {self.file_path}: {e}")
            import traceback
            traceback.print_exc()
            self.previous_content = ""

        self._trigger_event(EventType.POST_READ, {"content_length": len(self.previous_content)})
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content template."""
        return self.agent_logic_core.get_default_content(filename=self.file_path.name)

    def think(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generic reasoning method that doesn't involve file updates."""
        self._state: AgentState = AgentState.THINKING
        if hasattr(self, 'registry') and self.registry:
            self.registry.emit("thought_stream", {"agent": self.__class__.__name__, "thought": prompt[:100]})

        import asyncio
        coro = self.run_subagent(f"Reasoning: {self.__class__.__name__}", prompt, system_prompt or self._system_prompt)

        # Handle async execution from sync context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If loop is already running, we can't block.
            # Phase 21: Create a task to avoid "never awaited" warning
            asyncio.create_task(coro)
            import logging
            logging.warning("BaseAgent.think() called from running loop. Returning empty string.")
            return ""

        try:
            result = loop.run_until_complete(coro)
            self._state: AgentState = AgentState.IDLE
            return result
        except RuntimeError as e:
            # Fallback if we really can't await
            import logging
            logging.error(f"BaseAgent.think() failed to await async result: {e}")
            return ""

    async def improve_content(self, prompt: str) -> str:
        """Use AI to improve the content."""
        self._state: AgentState = AgentState.PROCESSING
        self._trigger_event(EventType.PRE_IMPROVE, {"prompt": prompt})

        # Pre-processing: Preemption and Quotas
        await self._check_preemption()
        self.quotas.update_usage(cycles=1)

        # Cache check
        cache_key: str = self._generate_cache_key(prompt, self.previous_content)
        if self._config.cache_enabled and cache_key in BaseAgent._response_cache:
            self.current_content = BaseAgent._response_cache[cache_key].response
            return self.current_content

        try:
            # Memory Integration
            memory_docs = []
            if self.memory:
                memories = self.memory.query(prompt, n_results=3)
                memory_docs = [m.get("content", "") for m in memories]

            full_prompt = self.agent_logic_core.prepare_improvement_prompt(
                prompt, memory_docs, self._history_manager.get_messages(), self._system_prompt
            )

            async def backend_callable(p: str, sp: str | None = None, h: list[dict[str, str]] | None = None) -> str:
                return await self.run_subagent(f"Improve {self.file_path.stem}", p, self.previous_content)

            improvement = await self.strategy.execute(full_prompt, self.previous_content, backend_callable)
            improvement = self.agent_logic_core.finalize_improvement(improvement, self._post_processors)

            # Quality Check and Retry
            quality = self._score_response_quality(improvement)
            if quality.value <= ResponseQuality.POOR.value and self._config.retry_count > 0:
                for _ in range(self._config.retry_count):
                    improvement = await self.run_subagent(f"Retry {self.file_path.stem}", full_prompt, self.previous_content)
                    if self._score_response_quality(improvement).value >= ResponseQuality.ACCEPTABLE.value:
                        break

            self.current_content = improvement
            if self._config.cache_enabled:
                BaseAgent._response_cache[cache_key] = CacheEntry(cache_key, improvement, time.time(), quality.value)

            self.add_to_history(MessageRole.USER.value, prompt)
            self.add_to_history(MessageRole.ASSISTANT.value, improvement[:500])
            self._trigger_event(EventType.POST_IMPROVE, {"quality": quality.name})
            return self.current_content

        except Exception as e:
            logging.warning(f"Improvement failed: {e}")
            self.current_content = self.previous_content
            return self.current_content

    async def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        exceeded, reason = self.quotas.check_quotas()
        if exceeded: raise CycleInterrupt(reason)

        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab

        result: str | None = await asyncio.to_thread(ab.run_subagent, description, prompt, original_content)
        self.quotas.update_usage(len(prompt)//4, len(result or "")//4 if result else 0)

        if result is None: return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> dict[str, Any]:
        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab
        return ab.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab
        return ab.describe_backends()

    def _get_fallback_response(self) -> str:
        return self.agent_logic_core.get_fallback_response()

    def generate_diff(self) -> str:
        """Generate a unified diff between original and improved content.

        Returns:
            str: Unified diff string.
        """
        return self.core.calculate_diff(
            self.previous_content,
            self.current_content,
            filename=str(self.file_path)
        )

    def update_file(self) -> bool:
        """Write content back to disk."""
        content_to_write = self.current_content
        suffix = self.file_path.suffix.lower()
        if suffix in {'.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md'):
            content_to_write = self.core.fix_markdown(content_to_write)

        if not self.core.validate_content_safety(content_to_write):
            logging.error(f"Security violation detected in {self.file_path.name}")
            return False

        if getattr(self._config, 'dry_run', False):
            return self._write_dry_run_diff()

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(content_to_write, encoding='utf-8')
            return True
        except Exception as e:
            logging.error(f"File write failed: {e}")
            return False

    def _write_dry_run_diff(self) -> bool:
        """Saves a diff for verification without modifying the file."""
        diff = self.get_diff()
        if not diff: return True

        dry_run_dir = Path("temp/dry_runs")
        dry_run_dir.mkdir(parents=True, exist_ok=True)
        safe_name = str(self.file_path).replace("\\", "_").replace("/", "_").replace(":", "_")
        diff_path = dry_run_dir / f"{safe_name}_{int(time.time())}.diff"

        try:
            diff_path.write_text(diff, encoding='utf-8')
            logging.info(f"Dry-run diff saved to {diff_path}")
            return True
        except Exception:
            return False

    def get_diff(self) -> str:
        return self.generate_diff()

    # ========== Prompt Templates ==========

    @classmethod
    def register_template(cls, template: PromptTemplate) -> None:
        """Register a prompt template for reuse.

        Args:
            template: The prompt template to register.
        """
        cls._prompt_templates[template.id] = template
        logging.debug(f"Registered template: {template.id}")

    @classmethod
    def get_template(cls, template_id: str) -> PromptTemplate | None:
        """Get a registered prompt template by ID.

        Args:
            template_id: The template ID to look up.

        Returns:
            The template if found, None otherwise.
        """
        return cls._prompt_templates.get(template_id)

    def improve_with_template(self, template_id: str, variables: dict[str, str]) -> str:
        """Improve content using a registered template.

        Args:
            template_id: ID of the template to use.
            variables: Variables to substitute in the template.

        Returns:
            Improved content.

        Raises:
            ValueError: If template not found.
        """
        template: PromptTemplate | None = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        prompt: str = template.template.format(**variables, content=self.previous_content)
        return self.improve_content(prompt)

    # ========== Conversation History ==========

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to conversation history.

        Args:
            role: Message role (user, assistant, system).
            content: Message content.
        """
        self._history_manager.add_message(role, content)

    def clear_history(self) -> None:
        """Clear conversation history."""
        self._history_manager.clear()

    def get_history(self) -> list[ConversationMessage]:
        """Get conversation history."""
        return self._history_manager.get_messages()

    def _build_prompt_with_history(self, prompt: str) -> str:
        """Build prompt with conversation history context. (Delegated to Core)."""
        return self._history_manager.build_prompt(prompt, self.agent_logic_core, self.core)

    # ========== Response Post-Processing ==========

    def add_post_processor(self, processor: Callable[[str], str]) -> None:
        """Add a response post-processor.

        Args:
            processor: Function that transforms response content.
        """
        self._post_processors.append(processor)
        logging.debug(f"Added post-processor: {processor.__name__}")

    @as_tool(category="cognition", priority=5)
    def take_note(self, note: str) -> str:
        """
        Record a persistent note into the internal scratchpad.
        Useful for modular thinking across multiple tool calls.
        """
        return self._scratchpad_manager.take_note(note, self.__class__.__name__)

    @as_tool(category="cognition")
    def get_notes(self) -> str:
        """Retrieves all notes from the persistent scratchpad."""
        return self._scratchpad_manager.get_notes()

    @as_tool(category="cognition")
    def clear_notes(self) -> str:
        """Clears the persistent scratchpad."""
        return self._scratchpad_manager.clear_notes()

    def clear_post_processors(self) -> None:
        """Clear all post-processors."""
        self._post_processors.clear()

    def _score_response_quality(self, response: str) -> ResponseQuality:
        return ResponseQuality(self.core.score_response_quality(response))

    def _generate_cache_key(self, prompt: str, content: str) -> str:
        return self.core.generate_cache_key(prompt, content, model=self._model or "")

    @classmethod
    def clear_cache(cls) -> None:
        cls._response_cache.clear()

    @classmethod
    def get_cache_stats(cls) -> dict[str, Any]:
        return BaseAgentCore().get_cache_stats(cls._response_cache)

    def get_token_usage(self) -> int:
        return self._token_usage

    def check_token_budget(self, estimated_tokens: int) -> bool:
        return self.agent_logic_core.check_token_budget(
            self._token_usage, estimated_tokens, self._config.token_budget
        )

    @classmethod
    def register_hook(cls, event: EventType, callback: EventHook) -> None:
        if event not in cls._event_hooks: cls._event_hooks[event] = []
        cls._event_hooks[event].append(callback)

    @classmethod
    def unregister_hook(cls, event: EventType, callback: EventHook) -> None:
        if event in cls._event_hooks and callback in cls._event_hooks[event]:
            cls._event_hooks[event].remove(callback)

    def _record(self, prompt: str, result: str, provider: str = "auto", model: str = "auto", meta: dict[str, Any] | None = None) -> None:
        try:
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(provider, model, prompt, result, meta)
        except Exception: pass

    def _trigger_event(self, event: EventType, data: dict[str, Any]) -> None:
        data["agent"], data["file_path"] = self.__class__.__name__, str(self.file_path)
        self.agent_logic_core.trigger_event(event, data, self._event_hooks.get(event, []))

    @classmethod
    def register_plugin(cls, name: str, plugin: Any) -> None:
        cls._plugins[name] = plugin

    @classmethod
    def get_plugin(cls, name: str) -> Any | None:
        return cls._plugins.get(name)

    @classmethod
    def health_check(cls) -> HealthCheckResult:
        healthy, details = BaseAgentCore().perform_health_check(
            cls.get_backend_status(), len(cls._response_cache), list(cls._plugins.keys())
        )
        return HealthCheckResult(healthy=healthy, backend_available=healthy, details=details)

    def save_state(self, path: Path | None = None) -> None:
        AgentStateManager.save_state(self.file_path, self._state.value, self._token_usage, self._state_data, len(self._history_manager.get_messages()), path)

    def load_state(self, path: Path | None = None) -> bool:
        state = AgentStateManager.load_state(self.file_path, path)
        if state:
            self._token_usage, self._state_data = state.get("token_usage", 0), state.get("state_data", {})
            return True
        return False

    # ========== Context Window Management ==========

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return self.core.estimate_tokens(text)

    def truncate_for_context(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit."""
        return self.core.truncate_for_context(text, max_tokens)

    # ========== Agent Delegation ==========

    def delegate_to(self, agent_type: str, prompt: str, target_file: str | None = None) -> str:
        """Launches another agent to perform a sub-task."""
        return AgentDelegator.delegate(
            agent_type=agent_type,
            prompt=prompt,
            current_agent_name=self.__class__.__name__,
            current_file_path=self.file_path,
            current_model=self.get_model(),
            target_file=target_file
        )
