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
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Type, cast, TYPE_CHECKING

if TYPE_CHECKING:
    import agent_strategies

from .models import (
    AgentConfig,
    AgentState,
    AuthConfig,
    AuthMethod,
    BatchRequest,
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
    PromptTemplateManager,
    PromptVersion,
    ResponsePostProcessor,
    ResponseQuality,
    SerializationConfig,
    SerializationFormat,
    TokenBudget,
)
from .core import BaseCore

# Advanced components (Lazy loaded or optional)
try:
    from src.classes.agent.LongTermMemory import LongTermMemory
    from src.classes.orchestration.SignalRegistry import SignalRegistry
    from src.classes.orchestration.ToolRegistry import ToolRegistry
except (ImportError, ValueError):
    LongTermMemory = None
    SignalRegistry = None
    ToolRegistry = None

from src.classes.backend.LocalContextRecorder import LocalContextRecorder


def fix_markdown_content(content: str) -> str:
    """Fix markdown formatting in content."""
    # Basic markdown fixes - can be extended
    return content


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on environment variable and argument.

    Sets up Python's logging system with level determined by environment
    variable (DV_AGENT_VERBOSITY) and / or command - line argument.

    Args:
        verbosity_arg: Verbosity level from --verbose argument (0-3).
                      Levels: 0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG.
                      Defaults to 0 (ERROR).

    Returns:
        None. Configures the global logging system.

    Environment Variables:
        DV_AGENT_VERBOSITY: Can be set to 'quiet', 'minimal', 'normal', or 'elaborate'.

    Note:
        - verbosity_arg takes precedence when provided and forces DEBUG level
        - Environment variable is used as fallback
        - Defaults to INFO level if neither is set
    """
    env_verbosity: str | None = os.environ.get('DV_AGENT_VERBOSITY')
    levels: Dict[str, int] = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    # Determine level from environment
    if env_verbosity:
        level: int = levels.get(env_verbosity.lower(), logging.WARNING)
    else:
        # Default to WARNING to reduce noise, as requested by self-improvement phase
        level: int = logging.WARNING
    # If argument is provided, it forces DEBUG (elaborate)
    if verbosity_arg > 0:
        level: int = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")


DEFAULT_PROMPT_TEMPLATES: List[PromptTemplate] = [
    PromptTemplate(
        id="improve_code",
        name="Code Improvement",
        template="Improve the following code:\n\n{content}\n\nFocus on: {focus}",
        description="General code improvement template",
        tags=["code", "improvement"]
    ),
    PromptTemplate(
        id="add_docstrings",
        name="Add Docstrings",
        template="Add comprehensive docstrings to all functions and classes:\n\n{content}",
        description="Template for adding documentation",
        tags=["documentation"]
    ),
    PromptTemplate(
        id="fix_bugs",
        name="Bug Fix",
        template="Analyze and fix bugs in this code:\n\n{content}\n\nKnown issues: {issues}",
        description="Template for bug fixing",
        tags=["bugs", "fix"]
    ),
    PromptTemplate(
        id="add_tests",
        name="Generate Tests",
        template="Generate comprehensive tests for:\n\n{content}\n\nCoverage focus: {coverage}",
        description="Template for test generation",
        tags=["tests", "coverage"]
    ),
]


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
        
        # Strategy for agent execution
        import agent_strategies
        self.strategy: agent_strategies.AgentStrategy = agent_strategies.DirectStrategy()

        # New attributes for enhanced functionality
        self._state: AgentState = AgentState.INITIALIZED
        self._conversation_history: List[ConversationMessage] = []
        self._config: AgentConfig = self._load_config()
        self._token_usage = 0
        self._state_data: Dict[str, Any] = {}
        self._post_processors: List[Callable[[str], str]] = []
        self._model: Optional[str] = None
        self._is_stop_requested = False
        
        # Determine Workspace Root (Phase 108: Robust detection delegated to Core)
        self._workspace_root = BaseCore.detect_workspace_root(self.file_path)
        
        self._local_global_context = None

        # Initialize Core Logic (Potential Rust Target)
        self.core = BaseCore(workspace_root=self._workspace_root)

        # Advanced features
        self.memory: LongTermMemory | None = LongTermMemory() if LongTermMemory else None
        self.registry: SignalRegistry | None = SignalRegistry() if SignalRegistry else None
        self.tool_registry: ToolRegistry | None = ToolRegistry() if ToolRegistry else None

        # Intelligence Harvesting (Phase 108)
        self.recorder = LocalContextRecorder(Path(self._workspace_root), f"{self.__class__.__name__}_Agent")

    @property
    def global_context(self) -> str:
        """Lazy-loaded GlobalContextEngine, preferring Fleet's shared instance."""
        # Prefer fleet-injected context
        if hasattr(self, 'fleet') and self.fleet and hasattr(self.fleet, 'global_context'):
            return self.fleet.global_context
            
        # Fallback to local lazy loading
        if self._local_global_context is None:
             try:
                from src.classes.context.GlobalContextEngine import GlobalContextEngine
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
                logging.debug(f"Registered tool {name} for {self.__class__.__name__} (Priority: {priority})")

    def _register_tools(self) -> None:
        """Automatically registers public methods with the ToolRegistry."""
        if not self.tool_registry:
            return
            
        self.register_tools(self.tool_registry)
        
        # Also register the core capability if not already there
        agent_name: str = self.__class__.__name__
        if not self.tool_registry.get_tool(agent_name):
             self.tool_registry.register_tool(agent_name, self.improve_content, category="core", priority=-1)

    def _load_config(self) -> AgentConfig:
        """Load agent configuration from environment variables.

        Returns:
            AgentConfig: Configuration object with settings from env vars.
        """
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

    def set_strategy(self, strategy: agent_strategies.AgentStrategy) -> None:
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
                    pass
                
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
                pass

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
            import agent_backend as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            import agent_backend as ab
        
        result: Optional[str] = ab.run_subagent(description, prompt, original_content)
        if result is None:
            logging.warning("Subagent returned None, using fallback response")
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
            import agent_backend as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            import agent_backend as ab
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
            import agent_backend as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent))
            import agent_backend as ab
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

        # Include last few messages for context
        recent: List[ConversationMessage] = self._conversation_history[-6:]  # Last 3 exchanges
        context_lines: List[str] = []
        for msg in recent:
            context_lines.append(f"[{msg.role}]: {msg.content[:200]}...")

        return f"Previous context:\n{''.join(context_lines)}\n\nCurrent request:\n{prompt}"

    # ========== Response Post-Processing ==========

    def add_post_processor(self, processor: Callable[[str], str]) -> None:
        """Add a response post-processor.

        Args:
            processor: Function that transforms response content.
        """
        self._post_processors.append(processor)
        logging.debug(f"Added post-processor: {processor.__name__}")

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
        """Save agent state to disk.

        Args:
            path: Path to save state file. Defaults to {file_path}.state.json.
        """
        state_path: Path = path or self.file_path.with_suffix(".state.json")
        state: Dict[str, Any] = {
            "file_path": str(self.file_path),
            "state": self._state.value,
            "token_usage": self._token_usage,
            "state_data": self._state_data,
            "history_length": len(self._conversation_history),
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        logging.debug(f"State saved to {state_path}")

    def load_state(self, path: Optional[Path] = None) -> bool:
        """Load agent state from disk.

        Args:
            path: Path to state file. Defaults to {file_path}.state.json.

        Returns:
            True if state loaded successfully.
        """
        state_path: Path = path or self.file_path.with_suffix(".state.json")
        if not state_path.exists():
            return False

        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self._token_usage = state.get("token_usage", 0)
            self._state_data = state.get("state_data", {})
            logging.debug(f"State loaded from {state_path}")
            return True
        except Exception as e:
            logging.warning(f"Failed to load state: {e}")
            return False

    # ========== Context Window Management ==========

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to estimate.

        Returns:
            Estimated token count (rough approximation).
        """
        return self.core.estimate_tokens(text)

    def truncate_for_context(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit.

        Args:
            text: Text to truncate.
            max_tokens: Maximum tokens allowed.

        Returns:
            Truncated text with ellipsis if truncated.
        """
        return self.core.truncate_for_context(text, max_tokens)

    # ========== Agent Delegation ==========

    def delegate_to(self, agent_type: str, prompt: str, target_file: Optional[str] = None) -> str:
        """Launches another agent to perform a sub-task.
        
        Args:
            agent_type: Type of agent to delegate to (e.g. 'CoderAgent', 'SearchAgent').
            prompt: The specific task or instruction for the sub-agent.
            target_file: Optional target file path (defaults to current agent's file).
            
        Returns:
            The result of the sub-agent's execution or an error message.
        """
        if getattr(self, "_no_cascade", False) or os.environ.get("DV_AGENT_PARENT"):
            logging.warning(f"Delegation to {agent_type} blocked by no-cascade setting.")
            return "Error: Delegation blocked by no-cascade policy."

        logging.info(f"Delegating task to {agent_type} for {target_file or self.file_path}")
        
        # Determine the target file
        target_path: Path = Path(target_file) if target_file else self.file_path
        
        try:
            # Dynamic discovery of agent classes
            # Expected pattern: src.classes.<type_lower>.<type>Agent
            # e.g. src.classes.coder.CoderAgent
            type_clean: str = agent_type.replace("Agent", "").lower()
            module_name: str = f"src.classes.{type_clean}.{agent_type}"
            
            import importlib
            module: sys.ModuleType = importlib.import_module(module_name)
            agent_class = getattr(module, agent_type)
            
            # Instantiate and run the agent
            # We set a parent environment variable to prevent infinite loops
            os.environ["DV_AGENT_PARENT"] = self.__class__.__name__
            
            try:
                with agent_class(str(target_path)) as sub_agent:
                    # Sync common configurations
                    if self.get_model():
                        sub_agent.set_model(self.get_model())
                    
                    # Run the sub-task
                    # Note: We use the prompt as context/input
                    result = sub_agent.improve_content(prompt)
                    sub_agent.update_file()
                    
                    logging.info(f"Delegation to {agent_type} completed successfully.")
                    return result
            finally:
                # Clear parent flag
                if os.environ.get("DV_AGENT_PARENT") == self.__class__.__name__:
                    del os.environ["DV_AGENT_PARENT"]
                
        except Exception as e:
            logging.error(f"Delegation to {agent_type} failed: {e}")
            return f"Error: Delegation failed - {str(e)}"
