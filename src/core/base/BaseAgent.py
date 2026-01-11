#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""BaseAgent main class and core agent logic."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import logging
from src.core.base.ConnectivityManager import ConnectivityManager
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Type, cast, TYPE_CHECKING

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

from src.core.base.models import (
    AgentConfig,
    AgentState,
    AgentType,
    AgentEvent,
    AuthConfig,
    AuthMethod,
    CacheEntry,
    ConversationHistory,
    ConversationMessage,
    EventHook,
    EventType,
    FilePriority,
    FilePriorityConfig,
    HealthCheckResult,
    InputType,
    MessageRole,
    ModelConfig,
    MultimodalInput,
    PromptTemplate,
    ResponseQuality,
    SerializationConfig,
    SerializationFormat,
    TokenBudget,
    BatchResult,
    ComposedAgent,
    ContextWindow,
    MultimodalBuilder,
    AgentPipeline,
    AgentParallel,
    AgentRouter,
    ConfigProfile,
)
from src.core.base.managers import (
    PromptTemplateManager,
    PromptVersion,
    PromptVersionManager,
    BatchRequest,
    RequestBatcher,
    AuthenticationManager,
    AuthManager,
    ResponsePostProcessor,
    MultimodalProcessor,
    AgentComposer,
    SerializationManager,
    FilePriorityManager,
    ResponseCache,
    StatePersistence,
    ModelSelector,
    QualityScorer,
    ABTest,
    EventManager,
    HealthChecker,
    PluginManager,
    ProfileManager,
)

from src.core.base.core import BaseCore
from src.core.base.state import AgentStateManager
from src.core.base.verification import AgentVerifier
from src.core.base.delegation import AgentDelegator
from src.core.base.shell import ShellExecutor

# Advanced components (Lazy loaded or optional)
try:
    from src.logic.agents.cognitive.LongTermMemory import LongTermMemory
    from src.infrastructure.orchestration.SignalRegistry import SignalRegistry
    from src.infrastructure.orchestration.ToolRegistry import ToolRegistry
except (ImportError, ValueError):
    LongTermMemory = None
    SignalRegistry = None
    ToolRegistry = None

from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from .logging_config import setup_logging
from .defaults import DEFAULT_PROMPT_TEMPLATES


def fix_markdown_content(content: str) -> str:
    """Fix markdown formatting in content."""
    # Basic markdown fixes - can be extended
    return content


# Advanced components (Lazy loaded or optional)


class BaseAgent:
    """Base class for all AI-powered agents.

    Provides common functionality for agents that use AI backends to improve
    code files, documentation, tests, and other artifacts. Handles file I/O,
    diff generation, and integration with AI services.

    Supports context manager protocol for automatic resource cleanup.

    Attributes:
        file_path (Path): Path to the file being improved.
        previous_content (str): Original file content before improvements.
        current_content (str): Improved file content after agent processing.

    Subclasses:
        - CoderAgent: Improves source code files
        - TestsAgent: Generates and improves test files
        - ChangesAgent: Manages changelog documentation
        - ContextAgent: Manages context/description files
        - ErrorsAgent: Analyzes and documents errors
        - ImprovementsAgent: Suggests code improvements
        - StatsAgent: Collects and reports statistics

    Example:
        class MyAgent(BaseAgent):
            def _get_default_content(self) -> bool:
                return "# New File\\n"

        with MyAgent('path/to/file.md') as agent:
            agent.improve_content("Make it better")
            agent.update_file()

    Note:
        - Automatically detects markdown files for formatting cleanup
        - Provides fallback responses when AI backend unavailable
        - Supports multiple AI backends via agent_backend module
        - Can be used as context manager for automatic cleanup
    """

    # Class-level attributes for shared state
    _prompt_templates: Dict[str, PromptTemplate] = {}
    _response_cache: Dict[str, CacheEntry] = {}
    _plugins: Dict[str, Any] = {}
    _event_hooks: Dict[EventType, List[Callable[[Dict[str, Any]], None]]] = {}

    def __init__(self, file_path: str) -> None:
        """Initialize the BaseAgent with file path.

        Args:
            file_path: Path to the file to improve. Can be absolute or relative.
                      Will be converted to pathlib.Path object.

        Note:
            Automatically reads previous content on initialization.
            Supports context manager protocol via __enter__ and __exit__.
        """
        self.file_path = Path(file_path)
        self.previous_content: str = ""
        self.current_content: str = ""
        self.fleet: Any = None # FleetManager reference
        
        # Knowledge Trinity initialization (Phase 126)
        try:
            from src.core.knowledge.knowledge_engine import KnowledgeEngine
            agent_name = self.__class__.__name__.lower().replace("agent", "") or "base"
            self.knowledge = KnowledgeEngine(agent_id=agent_name, base_path=Path("data/agents"))
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None
        
        # Strategy for agent execution (Phase 130: Lazy-loaded to avoid core-on-logic dependency)
        self._strategy: Optional[Any] = None

        # New attributes for enhanced functionality
        self._state: AgentState = AgentState.INITIALIZED
        self._conversation_history: List[ConversationMessage] = []
        self._scratchpad: List[str] = [] # Confucius-style persistent notes (Phase 128)
        self._config: AgentConfig = self._load_config()
        self._token_usage = 0
        self._state_data: Dict[str, Any] = {}
        self._post_processors: List[Callable[[str], str]] = []
        self._model: Optional[str] = None
        self._is_stop_requested = False
        self._system_prompt: str = "You are a helpful AI assistant."
        
        # Determine Workspace Root (Phase 108: Robust detection delegated to Core)
        self._workspace_root = BaseCore.detect_workspace_root(self.file_path)
        
        self._local_global_context = None

        # Initialize Core Logic (Potential Rust Target)
        self.core = BaseCore(workspace_root=self._workspace_root)

        # Advanced features
        # Derive agent name for data isolation (e.g., CoderAgent -> "coder")
        agent_name = self.__class__.__name__.lower().replace("agent", "") or "base"
        self.memory: LongTermMemory | None = LongTermMemory(agent_name=agent_name) if LongTermMemory else None
        
        self.registry: SignalRegistry | None = SignalRegistry() if SignalRegistry else None
        self.tool_registry: ToolRegistry | None = ToolRegistry() if ToolRegistry else None

        # Intelligence Harvesting (Phase 108)
        self.recorder = LocalContextRecorder(Path(self._workspace_root), f"{self.__class__.__name__}_Agent")

    @property
    def strategy(self) -> Any:
        """Strategy for agent execution (Phase 130: Lazy-loaded to avoid core-on-logic dependency)."""
        if not hasattr(self, "_strategy") or self._strategy is None:
            # Deferred import to break core-on-logic dependency
            try:
                from src.logic.strategies import plan_executor as agent_strategies
                self._strategy = agent_strategies.DirectStrategy()
            except (ImportError, ModuleNotFoundError):
                # Fallback if logic is not available
                self._strategy = None
        return self._strategy

    @strategy.setter
    def strategy(self, value: Any) -> None:
        self._strategy = value

    def _run_command(self, cmd: List[str], timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""
        return ShellExecutor.run_command(
            cmd=cmd,
            workspace_root=self._workspace_root,
            agent_name=self.__class__.__name__,
            models_config=getattr(self, 'models', None),
            recorder=getattr(self, 'recorder', None),
            timeout=timeout,
            max_retries=max_retries
        )

    @property
    def global_context(self) -> str:
        """Lazy-loaded GlobalContextEngine, preferring Fleet's shared instance."""
        # Prefer fleet-injected context
        if hasattr(self, 'fleet') and self.fleet and hasattr(self.fleet, 'global_context'):
            return self.fleet.global_context
            
        # Fallback to local lazy loading
        if self._local_global_context is None:
             try:
                from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine
                self._local_global_context = GlobalContextEngine(self._workspace_root)
             except (ImportError, ValueError):
                pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        self._local_global_context = value

    def register_tools(self, registry: 'ToolRegistry') -> None:
        """
        Registers all methods decorated with @as_tool with the provided registry.
        """
        if not registry:
            return

        import inspect
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, '_is_tool') and method._is_tool:
                # Default category from class name (e.g. LinguisticAgent -> linguistic)
                category: str = self.__class__.__name__.replace('Agent', '').lower()
                
                # Check for explicit category overridden on method
                if hasattr(method, '_tool_category'):
                    category = method._tool_category
                
                # Check for priority
                priority: int = getattr(method, '_tool_priority', 0)
                    
                registry.register_tool(
                    func=method,
                    owner_name=self.__class__.__name__,
                    category=category,
                    priority=priority
                )

    def calculate_anchoring_strength(self, result: str) -> float:
        """
        Calculates the 'Anchoring Strength' metric (Stanford Research 2025).
        Measures how well the output is anchored to the provided context/grounding.
        Returns a score between 0.0 and 1.0.
        """
        if not hasattr(self, 'context_pool') or not self.context_pool:
            return 0.5 # Default middle-ground if no context
            
        context_text = " ".join([str(v) for v in self.context_pool.values()])
        if not context_text:
            return 0.5
            
        # Basic implementation: calculate keyword overlap or semantic proximity
        # For Phase 126, we use a simple N-gram overlap as a proxy for anchoring.
        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0
            
        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)
        
        # Adjust for length - very short responses are often "unanchored" chat
        if len(result_words) < 5:
            score *= 0.5
            
        return min(1.0, score * 1.5) # Amplify slightly as non-context words are expected

    def calculate_anchoring_strength(self, result: str) -> float:
        """
        Calculates the 'Anchoring Strength' metric (Stanford Research 2025).
        """
        return AgentVerifier.calculate_anchoring_strength(result, getattr(self, 'context_pool', {}))

    def verify_self(self, result: str) -> tuple[bool, str]:
        """
        Self-verification layer (inspired by Keio University 2026 research).
        """
        anchoring_score = self.calculate_anchoring_strength(result)
        return AgentVerifier.verify_self(result, anchoring_score)

    def _load_config(self) -> AgentConfig:
        """Load agent configuration from environment variables."""
        return AgentConfig(
            backend=os.environ.get("DV_AGENT_BACKEND", "auto"),
            model=os.environ.get("DV_AGENT_MODEL", ""),
            max_tokens=int(os.environ.get("DV_AGENT_MAX_TOKENS", "4096")),
            temperature=float(os.environ.get("DV_AGENT_TEMPERATURE", "0.7")),
            retry_count=int(os.environ.get("DV_AGENT_RETRY_COUNT", "3")),
            timeout=int(os.environ.get("DV_AGENT_TIMEOUT", "60")),
            cache_enabled=os.environ.get("DV_AGENT_CACHE", "true").lower() == "true",
            token_budget=int(os.environ.get("DV_AGENT_TOKEN_BUDGET", "100000")),
        )

    def set_strategy(self, strategy: Any) -> None:
        """Set the reasoning strategy for the agent.

        Args:
            strategy: An instance of AgentStrategy (e.g., DirectStrategy, ChainOfThoughtStrategy).
        """
        self.strategy = strategy
        logging.info(f"Agent strategy set to {strategy.__class__.__name__}")

    @property
    def state(self) -> AgentState:
        """Get current agent state."""
        return self._state

    def set_model(self, model: str) -> None:
        """Set the model to use for this agent.

        Args:
            model: Model identifier (e.g., "gpt-4", "claude-3").
        """
        self._model = model
        logging.debug(f"Model set to: {model}")

    def _track_tokens(self, input_tokens: int, output_tokens: int) -> None:
        """Simulates recording token usage for telemetry."""
        self._last_token_usage = {
            "input": input_tokens,
            "output": output_tokens,
            "model": self.get_model() or "gpt-4o"
        }

    def get_model(self) -> Optional[str]:
        """Get the currently configured model."""
        return self._model or self._config.model or None

    def __enter__(self) -> "BaseAgent":
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug(f"{self.__class__.__name__} entering context manager")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Context manager exit. Handles cleanup if needed.

        Note:
            - Logs any exceptions that occurred
            - Does not suppress exceptions
            - Can be overridden in subclasses for custom cleanup
        """
        logging.debug(f"{self.__class__.__name__} exiting context manager")
        if exc_type is not None:
            logging.error(f"Agent context error: {exc_type.__name__}: {exc_val}")
            self._state: AgentState = AgentState.ERROR
            self._trigger_event(EventType.ERROR, {"exception": exc_val})
        else:
            self._state: AgentState = AgentState.COMPLETED
        return False  # Don't suppress exceptions

    def stop(self) -> None:
        """Request the agent to stop its current operation."""
        logging.info(f"Stop requested for {self.__class__.__name__}")
        self._is_stop_requested = True

    def register_webhook(self, url: str) -> None:
        """Registers a webhook URL for notifications."""
        if not hasattr(self, '_webhooks'):
             self._webhooks = []
        if url not in self._webhooks:
            self._webhooks.append(url)

    def run(self, prompt: str = "") -> None:
        """Standard execution loop for the agent.
        
        This method is primarily used by the GUI to run any agent in a thread.
        It calls improve_content() and then update_file() if not stopped.
        """
        self._is_stop_requested = False
        try:
            self.improve_content(prompt)
            if not self._is_stop_requested:
                self.update_file()
            else:
                logging.info(f"Update skipped for {self.__class__.__name__} due to stop request.")
            
            # Phase 123: Trigger completion event for webhooks
            event_data = {
                "event": "agent_complete",
                "status": "success",
                "file": str(self.file_path),
                "timestamp": time.time()
            }
            webhooks = getattr(self, '_webhooks', [])
            for url in webhooks:
                try:
                    if HAS_REQUESTS and requests:
                        requests.post(url, json=event_data, timeout=5)
                        logging.info(f"Webhook sent to {url}")
                except Exception as e:
                    logging.error(f"Failed to send webhook to {url}: {e}")
                    
        except Exception as e:
            logging.error(f"Error running {self.__class__.__name__}: {e}")
            raise

    def read_previous_content(self) -> str:
        """Read the existing file content from disk.

        Reads the file specified by file_path, storing content in previous_content.
        If file doesn't exist, loads default content for new files.

        Returns:
            str: The read content (same as previous_content attribute).

        Raises:
            None. Logs errors but doesn't raise. Returns empty string on failure.

        Note:
            - Uses UTF-8 encoding
            - Handles missing files gracefully
            - Automatically handles encoding errors
        """
        self._state: AgentState = AgentState.READING
        self._trigger_event(EventType.PRE_READ, {"file_path": str(self.file_path)})

        if self.file_path.is_file():
            try:
                logging.debug(f"Reading content from {self.file_path}")
                self.previous_content: str = self.file_path.read_text(encoding='utf-8')
                logging.info(f"Read {len(self.previous_content)} bytes from {self.file_path.name}")
            except Exception as e:
                # Diagnostic logging for file read failures
                error_info = []
                if not os.access(self.file_path, os.R_OK):
                    error_info.append("Permission denied (Read)")
                try:
                    stats: os.stat_result = self.file_path.stat()
                    error_info.append(f"Size: {stats.st_size} bytes")
                except Exception:
                    logging.warning(f"Could not retrieve additional stats for {self.file_path}")
                
                diag_msg: str = f"Failed to read file {self.file_path}: {e}"
                if error_info:
                    diag_msg += f" ({'; '.join(error_info)})"
                logging.error(diag_msg)
                self.previous_content: str = ""
        elif self.file_path.is_dir():
            logging.debug(f"Target path {self.file_path} is a directory, using default content.")
            self.previous_content: str = self._get_default_content()
        else:
            logging.debug(f"File does not exist, using default content: {self.file_path}")
            self.previous_content: str = self._get_default_content()

        self._trigger_event(EventType.POST_READ, {"content_length": len(self.previous_content)})
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content for new files.

        Provides a template for new files when they don't exist yet.
        Override in subclasses to provide agent-specific defaults.

        Returns:
            str: Default content template for the file type.

        Example:
            class TestsAgent(BaseAgent):
                def _get_default_content(self) -> str:
                    return "# Tests\n\n# Add tests here\n"

        Note:
            Called automatically by read_previous_content() for missing files.
        """
        return self.core.get_default_content(filename=self.file_path.name)

    def think(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generic reasoning method that doesn't involve file updates.
        Useful for planning, data generation, or internal reasoning.
        """
        self._state: AgentState = AgentState.THINKING
        
        # Broadcast thought to SignalBus if available
        if hasattr(self, 'registry') and self.registry:
            try:
                # We can't use self.signal_bus directly here easily as it's in FleetManager usually
                # But we can emit a signal via the registry if it exists
                self.registry.emit("thought_stream", {
                    "agent": self.__class__.__name__,
                    "thought": prompt[:100] + "..."
                })
            except Exception:
                logging.debug("Registry signal emission failed in think().")

        description: str = f"Reasoning for {self.__class__.__name__}"
        result: str = self.run_subagent(description, prompt, system_prompt or self._system_prompt)
        
        self._state: AgentState = AgentState.IDLE
        return result

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the content.

        Calls the agent_backend with the previous content and a prompt,
        receives improved content, and stores it in current_content.

        Args:
            prompt: The prompt describing what improvements to make.
                   e.g., "Add comprehensive docstrings to all functions"

        Returns:
            str: The improved content (same as current_content attribute).

        Raises:
            None. Falls back to previous_content on error.

        Example:
            agent.improve_content("Improve error handling")
            print(agent.current_content)

        Note:
            - Overridable in subclasses for agent-specific behavior
            - Logs warnings on failure but doesn't raise
            - Falls back to original content if improvement fails
        """
        self._state: AgentState = AgentState.PROCESSING
        self._trigger_event(EventType.PRE_IMPROVE, {"prompt": prompt})

        # Check cache first if enabled
        cache_key: str = self._generate_cache_key(prompt, self.previous_content)
        if self._config.cache_enabled and cache_key in BaseAgent._response_cache:
            cached: CacheEntry = BaseAgent._response_cache[cache_key]
            cached.hit_count += 1
            logging.debug(f"Cache hit for prompt (hits: {cached.hit_count})")
            self.current_content: str = cached.response
            return self.current_content

        class_name: str = self.__class__.__name__.replace('Agent', '').lower()
        description: str = f"Improve the {class_name} for {self.file_path.stem}"
        try:
            logging.info(f"Improving content with prompt: {prompt[:50]}...")

            # Integrate Long-Term Memory
            memory_context: str = ""
            if self.memory:
                try:
                    memories: List[Dict[str, Any]] = self.memory.query(prompt, n_results=3)
                    if memories:
                        memory_docs: List[Any] = [m.get("content", "") for m in memories]
                        memory_context: str = "\n\n### Related Past Memories\n" + "\n".join(memory_docs)
                        logging.info(f"Found {len(memories)} relevant memories for context.")
                except Exception as me:
                    logging.warning(f"Memory retrieval failed: {me}")

            # Add conversation context if available
            full_prompt: str = self._build_prompt_with_history(prompt) + memory_context

            # Define backend callable for strategy
            def backend_callable(p: str, sp: Optional[str] = None, h: Optional[List[Dict[str, str]]] = None) -> str:
                return self.run_subagent(description, p, self.previous_content)

            # Execute strategy
            improvement: str = self.strategy.execute(
                prompt=full_prompt,
                context=self.previous_content,
                backend_call=backend_callable
            )

            # Apply post-processors
            for processor in self._post_processors:
                improvement: str = processor(improvement)

            # Score response quality
            quality: ResponseQuality = self._score_response_quality(improvement)

            # Retry if quality is poor
            if quality.value <= ResponseQuality.POOR.value and self._config.retry_count > 0:
                logging.warning(f"Response quality {quality.name}, retrying...")
                for _ in range(self._config.retry_count):
                    improvement: str = self.run_subagent(description, full_prompt, self.previous_content)
                    quality: ResponseQuality = self._score_response_quality(improvement)
                    if quality.value >= ResponseQuality.ACCEPTABLE.value:
                        break

            self.current_content: str = improvement

            # Cache the response
            if self._config.cache_enabled:
                BaseAgent._response_cache[cache_key] = CacheEntry(
                    key=cache_key,
                    response=improvement,
                    timestamp=time.time(),
                    quality_score=quality.value
                )

            # Add to conversation history
            self._conversation_history.append(ConversationMessage(role=MessageRole.USER, content=prompt))
            self._conversation_history.append(ConversationMessage(
                role=MessageRole.ASSISTANT, content=improvement[:500]))

            logging.info(f"Content improved successfully ({len(improvement)} bytes)")
            self._trigger_event(EventType.POST_IMPROVE, {"quality": quality.name})
            
            # Emit signal for success
            if self.registry:
                try:
                    self.registry.emit("improvement_ready", self.__class__.__name__, {
                        "file": str(self.file_path),
                        "prompt": prompt[:100]
                    })
                except Exception as se:
                    logging.warning(f"Signal emission failed: {se}")
            
            # Save to memory if significant
            if self.memory and len(self.current_content) > 100:
                try:
                    self.memory.store(
                        f"Agent {self.__class__.__name__} improved {self.file_path.name} based on prompt: {prompt[:100]}",
                        {"file": str(self.file_path), "action": "improve"}
                    )
                except Exception as me:
                    logging.warning(f"Memory storage failed: {me}")

            # Phase 108: Record interaction for logic harvesting
            self._record(
                prompt=f"Task: {description}\nContext: {prompt}\nMem: {memory_context[:100]}",
                result=self.current_content[:1000] + ("..." if len(self.current_content) > 1000 else ""),
                provider="AI-Backend",
                model=self.__class__.__name__
            )

            return self.current_content
        except Exception as e:
            logging.warning(f"Failed to improve content: {e}")
            
            # Emit signal for failure
            if self.registry:
                try:
                    self.registry.emit("agent_fail", self.__class__.__name__, {
                        "file": str(self.file_path),
                        "error": str(e)
                    })
                except Exception as se:
                    pass

            self.current_content: str = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """Run a subagent using one of several AI backends.

        Delegates to agent_backend.run_subagent which selects the appropriate
        AI backend (copilot, GitHub Models, etc.) and executes the request.

        Args:
            description: Human-readable description of the task.
            prompt: The prompt to send to the AI backend.
            original_content: The content being improved (context for AI).
                            Defaults to empty string.

        Returns:
            str: Response from the AI backend, or fallback if unavailable.

        Raises:
            None. Returns fallback response on error.

        Note:
            - Backend selection is automatic or via DV_AGENT_BACKEND env var
            - Supports multiple backends: copilot, GitHub Models, local
            - Returns original_content as fallback if backend unavailable
        """
        logging.debug(f"Running subagent: {description}")
        # Deferred import to avoid circular dependency
        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab
        
        result: Optional[str] = ab.run_subagent(description, prompt, original_content)
        if result is None:
            # Lowered logging level to INFO (Phase 123)
            logging.info("Subagent returned None, using fallback response")
            return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> Dict[str, Any]:
        """Return a diagnostic snapshot of backend availability and configuration.

        Returns:
            dict: Status information for all available AI backends.
                 Includes availability, version, and configuration details.

        Example:
            status=BaseAgent.get_backend_status()
            for backend, info in status.items():
                print(f"{backend}: {info}")
        """
        logging.debug("Fetching backend status")
        # Deferred import to avoid circular dependency
        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab
        return ab.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        """Return human-readable backend diagnostics for debugging.

        Returns:
            str: Formatted text describing available backends and their status.
                 Useful for troubleshooting configuration issues.

        Example:
            print(BaseAgent.describe_backends())
            # Output: Available backends, versions, configuration details
        """
        logging.debug("Describing backend configuration")
        # Deferred import to avoid circular dependency
        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab
        return ab.describe_backends()

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot CLI is unavailable.

        Called when AI backend is not available. Override in subclasses to provide
        agent-specific fallback content.

        Returns:
            str: Fallback response text with helpful instructions.

        Note:
            Called automatically by run_subagent() when backend unavailable.
            Subclasses should override to provide domain-specific defaults.
        """
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub Copilot CLI ('copilot') not found or failed.\n"
            "# Install Copilot CLI: https://github.com/github/copilot-cli\n"
            "# Windows: winget install GitHub.Copilot\n"
            "# npm: npm install -g @github/copilot\n"
        )

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
        """Write the improved content back to the file.

        Writes current_content to disk, with special handling for markdown files
        which get normalized/fixed using the fix_markdown_content function.

        Returns:
            bool: True if the file was written successfully.

        Raises:
            OSError: If file write fails.

        Note:
            - Automatically detects markdown files (.md, .markdown, .plan.md)
            - Applies markdown normalization only to markdown files
            - Uses UTF-8 encoding for all files
            - Creates parent directories if they don't exist

        Example:
            agent.current_content="# Improved Content"
            agent.update_file()  # Writes to agent.file_path
        """
        content_to_write: str = self.current_content
        # Only run the markdown fixer on markdown-like files. Applying markdown
        # normalization to source code can corrupt it.
        suffix: str = self.file_path.suffix.lower()
        is_markdown: bool = suffix in {
            '.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md')
        if is_markdown:
            logging.debug(f"Applying markdown formatting to {self.file_path.name}")
            content_to_write: str = self.core.fix_markdown(content_to_write)

        # Security Check: Validate content safety before writing (Phase 108)
        if not self.core.validate_content_safety(content_to_write):
            logging.error(f"Security violation detected in content for {self.file_path.name}. Write aborted!")
            return False

        logging.info(f"Writing {len(content_to_write)} bytes to {self.file_path.name}")
        # Ensure parent directory exists
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(content_to_write, encoding='utf-8')
            return True
        except Exception as e:
            logging.error(f"Self-Healing: File write failed for {self.file_path.name}: {e}")
            # Potential self-healing: Try to clear locks or use a temp file
            return False

    def get_diff(self) -> str:
        """Get the diff between previous and current content.

        Generates a unified diff showing what changed between the original
        and improved versions of the file.

        Returns:
            str: Unified diff format. Empty string if no changes.

        Example:
            diff=agent.get_diff()
            if diff:
                print("Changes made:")
                print(diff)
            else:
                print("No changes")

        Note:
            - Uses difflib.unified_diff for standard format
            - Preserves line endings in diff
            - Empty string indicates no changes between versions
        """
        logging.debug("Generating diff between previous and current content")
        diff_str: str = self.core.calculate_diff(
            self.previous_content,
            self.current_content,
            filename=self.file_path.name
        )
        if diff_str:
            logging.debug(f"Generated {len(diff_str)} bytes of diff")
        else:
            logging.debug("No differences found")
        return diff_str

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
    def get_template(cls, template_id: str) -> Optional[PromptTemplate]:
        """Get a registered prompt template by ID.

        Args:
            template_id: The template ID to look up.

        Returns:
            The template if found, None otherwise.
        """
        return cls._prompt_templates.get(template_id)

    def improve_with_template(self, template_id: str, variables: Dict[str, str]) -> str:
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
        role_value: str = role.strip().lower()
        try:
            role_enum = MessageRole(role_value)
        except ValueError:
            role_enum: MessageRole = MessageRole.SYSTEM
        self._conversation_history.append(ConversationMessage(role=role_enum, content=content))

    def clear_history(self) -> None:
        """Clear conversation history."""
        self._conversation_history.clear()
        logging.debug("Conversation history cleared")

    def get_history(self) -> List[ConversationMessage]:
        """Get conversation history."""
        return self._conversation_history.copy()

    def _build_prompt_with_history(self, prompt: str) -> str:
        """Build prompt with conversation history context.

        Args:
            prompt: The current prompt.

        Returns:
            Prompt with history context prepended.
        """
        if not self._conversation_history:
            return prompt

        history = [{"role": m.role.value, "content": m.content} for m in self._conversation_history]
        return self.core.build_prompt_with_history(prompt, history)

    # ========== Response Post-Processing ==========

    def add_post_processor(self, processor: Callable[[str], str]) -> None:
        """Add a response post-processor.

        Args:
            processor: Function that transforms response content.
        """
        self._post_processors.append(processor)
        logging.debug(f"Added post-processor: {processor.__name__}")

    def take_note(self, note: str) -> str:
        """
        Record a persistent note into the internal scratchpad.
        Useful for modular thinking across multiple tool calls.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_note = f"[{timestamp}] {note}"
        self._scratchpad.append(formatted_note)
        logging.info(f"Agent {self.__class__.__name__} took a note: {note}")
        return f"Note recorded: {note}"

    def get_notes(self) -> str:
        """Retrieves all notes from the persistent scratchpad."""
        if not self._scratchpad:
            return "No notes recorded yet."
        return "\n".join(self._scratchpad)

    def clear_notes(self) -> str:
        """Clears the persistent scratchpad."""
        self._scratchpad = []
        return "Scratchpad cleared."

    def clear_post_processors(self) -> None:
        """Clear all post-processors."""
        self._post_processors.clear()

    # ========== Response Quality Scoring ==========

    def _score_response_quality(self, response: str) -> ResponseQuality:
        """Score the quality of an AI response.

        Args:
            response: The response to score.

        Returns:
            Quality score enum value.
        """
        score: int = self.core.score_response_quality(response)
        return ResponseQuality(score)

    # ========== Cache Management ==========

    def _generate_cache_key(self, prompt: str, content: str) -> str:
        """Generate a content-based cache key.

        Args:
            prompt: The prompt.
            content: The content being processed.

        Returns:
            SHA256 hash key.
        """
        return self.core.generate_cache_key(prompt, content, model=self._model or "")

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the response cache."""
        cls._response_cache.clear()
        logging.debug("Response cache cleared")

    @classmethod
    def get_cache_stats(cls) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats.
        """
        total_hits: int = sum(e.hit_count for e in cls._response_cache.values())
        avg_quality: float = sum(
            e.quality_score for e in cls._response_cache.values()
        ) / max(len(cls._response_cache), 1)
        return {
            "entries": len(cls._response_cache),
            "total_hits": total_hits,
            "avg_quality": avg_quality
        }

    # ========== Token Budget Management ==========

    def get_token_usage(self) -> int:
        """Get total token usage for this session."""
        return self._token_usage

    def check_token_budget(self, estimated_tokens: int) -> bool:
        """Check if request fits within token budget.

        Args:
            estimated_tokens: Estimated tokens for the request.

        Returns:
            True if within budget, False otherwise.
        """
        return (self._token_usage + estimated_tokens) <= self._config.token_budget

    # ========== Event Hooks ==========

    @classmethod
    def register_hook(cls, event: EventType, callback: EventHook) -> None:
        """Register an event hook.

        Args:
            event: Event type to hook.
            callback: Callback function to invoke.
        """
        if event not in cls._event_hooks:
            cls._event_hooks[event] = []
        cls._event_hooks[event].append(callback)
        logging.debug(f"Registered hook for event: {event.value}")

    @classmethod
    def unregister_hook(cls, event: EventType, callback: EventHook) -> None:
        """Unregister an event hook.

        Args:
            event: Event type.
            callback: Callback to remove.
        """
        if event in cls._event_hooks and callback in cls._event_hooks[event]:
            cls._event_hooks[event].remove(callback)

    def _record(self, prompt: str, result: str, provider: str = "auto", model: str = "auto", meta: Dict[str, Any] = None) -> None:
        """Helper to record interactions to the LocalContextRecorder (Phase 108)."""
        try:
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    result=result,
                    meta=meta
                )
        except Exception as e:
            logging.debug(f"Interaction recording failed: {e}")

    def _trigger_event(self, event: EventType, data: Dict[str, Any]) -> None:
        """Trigger an event and invoke all registered hooks.

        Args:
            event: Event type.
            data: Event data to pass to hooks.
        """
        data["agent"] = self.__class__.__name__
        data["file_path"] = str(self.file_path)

        for callback in self._event_hooks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logging.warning(f"Hook error for {event.value}: {e}")

    # ========== Plugin System ==========

    @classmethod
    def register_plugin(cls, name: str, plugin: Any) -> None:
        """Register an agent plugin.

        Args:
            name: Plugin name.
            plugin: Plugin instance.
        """
        cls._plugins[name] = plugin
        logging.debug(f"Registered plugin: {name}")

    @classmethod
    def get_plugin(cls, name: str) -> Optional[Any]:
        """Get a registered plugin.

        Args:
            name: Plugin name.

        Returns:
            Plugin instance if found.
        """
        return cls._plugins.get(name)

    # ========== Health Checks ==========

    @classmethod
    def health_check(cls) -> HealthCheckResult:
        """Perform agent health check.

        Returns:
            HealthCheckResult with diagnostic information.
        """
        backend_status: Dict[str, Any] = cls.get_backend_status()
        backend_available: bool = any(
            cast(Dict[str, Any], v).get("available", False)
            for v in backend_status.values()
            if isinstance(v, dict)
        )

        return HealthCheckResult(
            healthy=backend_available,
            backend_available=backend_available,
            details={
                "backends": backend_status,
                "cache_entries": len(cls._response_cache),
                "plugins": list(cls._plugins.keys()),
            }
        )

    # ========== State Persistence ==========

    def save_state(self, path: Optional[Path] = None) -> None:
        """Save agent state to disk."""
        AgentStateManager.save_state(
            file_path=self.file_path,
            current_state=self._state.value,
            token_usage=self._token_usage,
            state_data=self._state_data,
            history_len=len(self._conversation_history),
            path=path
        )

    def load_state(self, path: Optional[Path] = None) -> bool:
        """Load agent state from disk."""
        state = AgentStateManager.load_state(self.file_path, path)
        if state:
            self._token_usage = state.get("token_usage", 0)
            self._state_data = state.get("state_data", {})
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

    def delegate_to(self, agent_type: str, prompt: str, target_file: Optional[str] = None) -> str:
        """Launches another agent to perform a sub-task."""
        return AgentDelegator.delegate(
            agent_type=agent_type,
            prompt=prompt,
            current_agent_name=self.__class__.__name__,
            current_file_path=self.file_path,
            current_model=self.get_model(),
            target_file=target_file
        )