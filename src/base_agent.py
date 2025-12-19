#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Base Agent: shared functionality for AI-powered file-improvement agents.

This module defines `BaseAgent`, which provides:

- File I/O helpers for reading an existing file (or generating default content).
- AI backend integration via `agent_backend` with caching, retries, and simple
    response quality scoring.
- Optional markdown normalization (only for markdown-like files) via the
    `fix_markdown_content` helper.
- Convenience utilities such as prompt templates, conversation history,
    post-processing hooks, health checks, and lightweight state persistence.

It also exposes `create_main_function()` to generate a small argparse-based CLI
wrapper for agents.
"""

import argparse
from typing import Any, Callable, Optional
try:
    import agent_strategies
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import agent_strategies

import difflib
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import sys
from types import TracebackType
from typing import Optional, Dict, List, Any, Callable, Type, cast
import hashlib
import time

try:
    import agent_backend as agent_backend
except ImportError:  # pragma: no cover
    # Last resort: try to find it relative to this file
    sys.path.append(str(Path(__file__).parent))
    import agent_backend as agent_backend


def _empty_list_str() -> list[str]:
    return []


def _empty_list_int() -> list[int]:
    return []


def _empty_list_float() -> list[float]:
    return []


def _empty_dict_str_any() -> dict[str, Any]:
    return {}


def _empty_dict_str_int() -> dict[str, int]:
    return {}


def _empty_dict_str_str() -> dict[str, str]:
    return {}


def _empty_dict_str_callable_any_any() -> dict[str, Callable[[Any], Any]]:
    return {}


def _empty_dict_str_quality_criteria() -> dict[str, tuple[Callable[[str], float], float]]:
    return {}


def _empty_dict_str_health_checks() -> dict[str, Callable[[], dict[str, Any]]]:
    return {}


def _empty_dict_str_configprofile() -> dict[str, "ConfigProfile"]:
    return {}


def _empty_routes_list() -> list[tuple[Callable[[Any], bool], Callable[[Any], Any]]]:
    return []


def _empty_dict_str_filepriority() -> dict[str, "FilePriority"]:
    return {}


def _empty_dict_str_modelconfig() -> dict[str, "ModelConfig"]:
    return {}


EventHook = Callable[[dict[str, Any]], None]


# ========== Enums for Type Safety ==========

class AgentState(Enum):
    """Agent lifecycle states."""
    INITIALIZED = "initialized"
    READING = "reading"
    PROCESSING = "processing"
    WRITING = "writing"
    COMPLETED = "completed"
    ERROR = "error"


class ResponseQuality(Enum):
    """AI response quality levels."""
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    INVALID = 1


class EventType(Enum):
    """Agent event types for hooks."""
    PRE_READ = "pre_read"
    POST_READ = "post_read"
    PRE_IMPROVE = "pre_improve"
    POST_IMPROVE = "post_improve"
    PRE_WRITE = "pre_write"
    POST_WRITE = "post_write"
    ERROR = "error"


class AuthMethod(Enum):
    """Authentication methods for backends."""
    NONE = "none"
    API_KEY = "api_key"
    TOKEN = "token"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"


class SerializationFormat(Enum):
    """Custom serialization formats."""
    JSON = "json"
    YAML = "yaml"
    MSGPACK = "msgpack"
    PICKLE = "pickle"
    PROTOBUF = "protobuf"


class FilePriority(Enum):
    """File priority levels for request prioritization."""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    BACKGROUND = 1


class InputType(Enum):
    """Input types for multimodal support."""
    TEXT = "text"
    IMAGE = "image"
    DIAGRAM = "diagram"
    CODE = "code"
    AUDIO = "audio"
    VIDEO = "video"


class AgentType(Enum):
    """Agent type classifications."""
    GENERAL = "general"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"


# ========== Dataclasses for Data Structures ==========

@dataclass
class PromptTemplate:
    """Reusable prompt template.

    Attributes:
        name: Human - readable template name.
        template: The prompt template with {placeholders}.
        variables: List of variable names in the template.
        id: Optional unique identifier for the template.
        description: Description of when to use this template.
        version: Version string for A / B testing.
        tags: Tags for categorization.
    """
    name: str
    template: str
    variables: List[str] = field(default_factory=_empty_list_str)
    id: str = ""
    description: str = ""
    version: str = "1.0"
    tags: List[str] = field(default_factory=_empty_list_str)

    def render(self, **kwargs: Any) -> str:
        """Render the template with provided variables.

        Args:
            **kwargs: Variables to substitute in the template.

        Returns:
            Rendered template string.
        """
        return self.template.format(**kwargs)


class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        """Register a prompt template.

        Args:
            template: PromptTemplate to register.
        """
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        """Render a template by name.

        Args:
            template_name: Name of the template to render.
            **kwargs: Variables to substitute in the template.

        Returns:
            Rendered template string.

        Raises:
            KeyError: If template not found.
        """
        template = self.templates[template_name]
        return template.render(**kwargs)


class MessageRole(Enum):
    """Roles for conversation messages."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ConversationMessage:
    """A message in conversation history.

    Attributes:
        role: The role (user, assistant, system).
        content: Message content.
        timestamp: When the message was created.
    """
    role: MessageRole
    content: str
    timestamp: float = field(default_factory=time.time)


class ConversationHistory:
    """Manages a conversation history with message storage and retrieval."""

    def __init__(self, max_messages: int = 100) -> None:
        """Initialize conversation history.

        Args:
            max_messages: Maximum number of messages to keep.
        """
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages

    def add(self, role: MessageRole, content: str) -> None:
        """Add a message to the history.

        Args:
            role: Message role (user, assistant, system).
            content: Message content.
        """
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)

        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> List[ConversationMessage]:
        """Get conversation context (all messages).

        Returns:
            List of conversation messages.
        """
        return self.messages.copy()

    def clear(self) -> None:
        """Clear all messages from history."""
        self.messages.clear()


class ResponsePostProcessor:
    """Manages post-processing hooks for agent responses."""

    def __init__(self) -> None:
        """Initialize the post-processor."""
        self.hooks: List[tuple[Callable[[str], str], int]] = []

    def register(self, hook: Callable[[str], str], priority: int = 0) -> None:
        """Register a post-processing hook.

        Args:
            hook: Function that takes text and returns processed text.
            priority: Priority level (higher = executed first).
        """
        self.hooks.append((hook, priority))

    def process(self, text: str) -> str:
        """Process text through all registered hooks in priority order.

        Args:
            text: Text to process.

        Returns:
            Processed text.
        """
        # Sort by priority (descending), then execute in order
        sorted_hooks = sorted(self.hooks, key=lambda x: x[1], reverse=True)
        for hook, _ in sorted_hooks:
            text = hook(text)
        return text


@dataclass
class CacheEntry:
    """Cached response entry.

    Attributes:
        key: Content - based cache key.
        response: Cached response content.
        timestamp: When the entry was cached.
        hit_count: Number of cache hits.
        quality_score: Quality score of response.
    """
    key: str
    response: str
    timestamp: float
    hit_count: int = 0
    quality_score: float = 0.0


@dataclass
class AgentConfig:
    """Agent configuration from environment or file.

    Attributes:
        backend: AI backend to use.
        model: Model name / ID for the backend.
        max_tokens: Maximum tokens per request.
        temperature: Sampling temperature.
        retry_count: Number of retries on failure.
        timeout: Request timeout in seconds.
        cache_enabled: Whether to enable response caching.
        token_budget: Total token budget for session.
    """
    backend: str = "auto"
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    retry_count: int = 3
    timeout: int = 60
    cache_enabled: bool = True
    token_budget: int = 100000


@dataclass
class HealthCheckResult:
    """Result of agent health check.

    Attributes:
        healthy: Overall health status.
        backend_available: Whether AI backend is available.
        memory_ok: Whether memory usage is acceptable.
        disk_ok: Whether disk space is sufficient.
        details: Additional health details.
    """
    healthy: bool
    backend_available: bool
    memory_ok: bool = True
    disk_ok: bool = True
    details: Dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass
class AuthConfig:
    """Authentication configuration.

    Attributes:
        method: Authentication method type.
        api_key: API key for API_KEY auth.
        token: Bearer token for token - based auth.
        username: Username for basic auth.
        password: Password for basic auth.
        oauth_client_id: OAuth2 client ID.
        oauth_client_secret: OAuth2 client secret.
        custom_headers: Custom headers to include.
    """
    method: AuthMethod = AuthMethod.NONE
    api_key: str = ""
    token: str = ""
    username: str = ""
    password: str = ""
    oauth_client_id: str = ""
    oauth_client_secret: str = ""
    custom_headers: Dict[str, str] = field(default_factory=_empty_dict_str_str)


class BatchRequest:
    """Request in a batch processing queue.

    Supports both generic batching (with items) and file-based batching.

    Attributes:
        file_path: Path to the file to process (optional).
        prompt: Improvement prompt (optional).
        priority: Processing priority.
        callback: Optional callback on completion.
        max_size: Maximum batch size (for generic batching).
        items: Items in the batch (for generic batching).
    """

    def __init__(
        self,
        file_path: Optional[Path] = None,
        prompt: Optional[str] = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
        max_size: Optional[int] = None
    ) -> None:
        """Initialize batch request.

        Supports both old file-based API and new generic batching API.

        Args:
            file_path: Path to file (old API).
            prompt: Prompt text (old API).
            priority: Processing priority (old API).
            callback: Completion callback (old API).
            max_size: Max items before flush (new API).
        """
        # Old API fields
        self.file_path = file_path
        self.prompt = prompt or ""
        self.priority = priority
        self.callback = callback

        # New API fields
        self.max_size = max_size
        self.items: List[Any] = []

    def add(self, item: Any) -> None:
        """Add item to batch (new API).

        Args:
            item: Item to add.
        """
        # If at max size, don't add
        if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        """Get batch size (new API)."""
        return len(self.items)

    def execute(self, processor: Callable[[List[Any]], List[Any]]) -> List[Any]:
        """Execute batch with processor (new API).

        Args:
            processor: Function to process batch items.

        Returns:
            Processed results.
        """
        return processor(self.items)


@dataclass
class BatchResult:
    """Result of a batch processing request.

    Attributes:
        file_path: Path to the processed file.
        success: Whether processing succeeded.
        content: Processed content if successful.
        error: Error message if failed.
        processing_time: Time taken to process.
    """
    file_path: Path | None
    success: bool
    content: str = ""
    error: str = ""
    processing_time: float = 0.0


@dataclass
class PromptVersion:
    """Versioned prompt for A/B testing.

    Supports both simple and advanced versioning APIs.

    Attributes:
        version: Version identifier.
        content: The prompt content.
        description: Prompt description.
        active: Whether this version is active.
        created_at: Creation timestamp.
        metrics: Performance metrics.
        version_id: Alias for version (compatibility).
        template_id: Template identifier (compatibility).
        variant: Variant name (compatibility).
        prompt_text: Alias for content (compatibility).
        weight: Selection weight (compatibility).
    """

    def __init__(
        self,
        version: Optional[str] = None,
        content: Optional[str] = None,
        description: str = "",
        active: bool = True,
        version_id: Optional[str] = None,
        template_id: Optional[str] = None,
        variant: Optional[str] = None,
        prompt_text: Optional[str] = None,
        weight: float = 1.0
    ) -> None:
        """Initialize prompt version.

        Supports both new and old parameter names for compatibility.

        Args:
            version: Version string (new API).
            content: Prompt content (new API).
            description: Optional description.
            active: Whether version is active.
            version_id: Version ID (old API, used if version is None).
            template_id: Template ID (old API).
            variant: Variant name (old API).
            prompt_text: Prompt text (old API, used if content is None).
            weight: Selection weight (old API).
        """
        # Support both APIs
        self.version = version or version_id or ""
        self.content = content or prompt_text or ""
        self.description = description
        self.active = active
        self.created_at = datetime.now()
        self.metrics: Dict[str, float] = {}

        # Old API compatibility
        self.version_id = self.version
        self.template_id = template_id or ""
        self.variant = variant or ""
        self.prompt_text = self.content
        self.weight = weight


@dataclass
class MultimodalInput:
    """Multimodal input for agents.

    Attributes:
        input_type: Type of input (text, image, etc.).
        content: Content data (text, base64, path).
        mime_type: MIME type for binary content.
        metadata: Additional input metadata.
    """
    input_type: InputType
    content: str
    mime_type: str = ""
    metadata: Dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass
class ComposedAgent:
    """Configuration for agent composition.

    Attributes:
        agent_type: Type of agent to use.
        config: Agent - specific configuration.
        order: Execution order in composition.
        depends_on: Other agents this depends on.
    """
    agent_type: str
    config: Dict[str, Any] = field(default_factory=_empty_dict_str_any)
    order: int = 0
    depends_on: List[str] = field(default_factory=_empty_list_str)


@dataclass
class SerializationConfig:
    """Configuration for custom serialization.

    Attributes:
        format: Serialization format.
        options: Format - specific options.
        compression: Whether to compress output.
        encryption: Whether to encrypt output.
    """
    format: SerializationFormat = SerializationFormat.JSON
    options: Dict[str, Any] = field(default_factory=_empty_dict_str_any)
    compression: bool = False
    encryption: bool = False


@dataclass
class FilePriorityConfig:
    """Configuration for file priority.

    Attributes:
        path_patterns: Patterns mapped to priorities.
        extension_priorities: Extensions mapped to priorities.
        default_priority: Default priority level.
    """
    path_patterns: Dict[str, FilePriority] = field(default_factory=_empty_dict_str_filepriority)
    extension_priorities: Dict[str, FilePriority] = field(default_factory=_empty_dict_str_filepriority)
    default_priority: FilePriority = FilePriority.NORMAL


# ========== Default Prompt Templates ==========

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
    env_verbosity = os.environ.get('DV_AGENT_VERBOSITY')
    levels = {
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
        level = levels.get(env_verbosity.lower(), logging.INFO)
    else:
        level = logging.INFO
    # If argument is provided, it forces DEBUG (elaborate)
    if verbosity_arg > 0:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")


# Import markdown fixing functionality (optional).
try:
    from scripts.fix.fix_markdown_lint import fix_markdown_content  # type: ignore
except ImportError:
    try:
        import importlib.util
        fix_dir = Path(__file__).parent.parent / 'fix'
        spec = importlib.util.spec_from_file_location(
            "fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["fix_markdown_lint"] = module
            spec.loader.exec_module(module)
            fix_markdown_content = module.fix_markdown_content
        else:
            raise ImportError
    except (ImportError, AttributeError):  # pragma: no cover
        def fix_markdown_content(text: str) -> str:
            return text


class BaseAgent:
    """Base class for all AI-powered agents.

    Provides common functionality for agents that use AI backends to improve
    code files, documentation, tests, and other artifacts. Handles file I / O,
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
        - ContextAgent: Manages context / description files
        - ErrorsAgent: Analyzes and documents errors
        - ImprovementsAgent: Suggests code improvements
        - StatsAgent: Collects and reports statistics

    Example:
        class MyAgent(BaseAgent):
            def _get_default_content(self):
                return "# New File\\n"

        with MyAgent('path / to / file.md') as agent:
            agent.improve_content("Make it better")
            agent.update_file()

    Note:
        - Automatically detects markdown files for formatting cleanup
        - Provides fallback responses when AI backend unavailable
        - Supports multiple AI backends via agent_backend module
        - Can be used as context manager for automatic cleanup
    """

    # Class - level attributes for shared state
    _prompt_templates: Dict[str, PromptTemplate] = {}
    _response_cache: Dict[str, CacheEntry] = {}
    _plugins: Dict[str, Any] = {}
    _event_hooks: Dict[EventType, List[EventHook]] = {e: cast(List[EventHook], []) for e in EventType}

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
        self.previous_content = ""
        self.current_content = ""
        
        # Strategy for agent execution
        self.strategy: agent_strategies.AgentStrategy = agent_strategies.DirectStrategy()

        # New attributes for enhanced functionality
        self._state = AgentState.INITIALIZED
        self._conversation_history: List[ConversationMessage] = []
        self._config = self._load_config()
        self._token_usage = 0
        self._state_data: Dict[str, Any] = {}
        self._post_processors: List[Callable[[str], str]] = []
        self._model: Optional[str] = None

        logging.debug(f"Initializing {self.__class__.__name__} for {file_path}")
        self.read_previous_content()

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
            self._state = AgentState.ERROR
            self._trigger_event(EventType.ERROR, {"exception": exc_val})
        else:
            self._state = AgentState.COMPLETED
        return False  # Don't suppress exceptions

    def read_previous_content(self) -> str:
        """Read the existing file content from disk.

        Reads the file specified by file_path, storing content in previous_content.
        If file doesn't exist, loads default content for new files.

        Returns:
            str: The read content (same as previous_content attribute).

        Raises:
            None. Logs errors but doesn't raise. Returns empty string on failure.

        Note:
            - Uses UTF - 8 encoding
            - Handles missing files gracefully
            - Automatically handles encoding errors
        """
        self._state = AgentState.READING
        self._trigger_event(EventType.PRE_READ, {"file_path": str(self.file_path)})

        if self.file_path.exists():
            try:
                logging.debug(f"Reading content from {self.file_path}")
                self.previous_content = self.file_path.read_text(encoding='utf-8')
                logging.info(f"Read {len(self.previous_content)} bytes from {self.file_path.name}")
            except Exception as e:
                logging.error(f"Failed to read file {self.file_path}: {e}")
                self.previous_content = ""
        else:
            logging.debug(f"File does not exist, using default content: {self.file_path}")
            self.previous_content = self._get_default_content()

        self._trigger_event(EventType.POST_READ, {"content_length": len(self.previous_content)})
        return self.previous_content

    def _get_default_content(self) -> str:
        """Return default content for new files.

        Provides a template for new files when they don't exist yet.
        Override in subclasses to provide agent - specific defaults.

        Returns:
            str: Default content template for the file type.

        Example:
            class TestsAgent(BaseAgent):
                def _get_default_content(self):
                    return "# Tests\\n\\n# Add tests here\\n"

        Note:
            Called automatically by read_previous_content() for missing files.
        """
        return "# Default content\n\n# Add content here\n"

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
            - Overridable in subclasses for agent - specific behavior
            - Logs warnings on failure but doesn't raise
            - Falls back to original content if improvement fails
        """
        self._state = AgentState.PROCESSING
        self._trigger_event(EventType.PRE_IMPROVE, {"prompt": prompt})

        # Check cache first if enabled
        cache_key = self._generate_cache_key(prompt, self.previous_content)
        if self._config.cache_enabled and cache_key in BaseAgent._response_cache:
            cached = BaseAgent._response_cache[cache_key]
            cached.hit_count += 1
            logging.debug(f"Cache hit for prompt (hits: {cached.hit_count})")
            self.current_content = cached.response
            return self.current_content

        class_name = self.__class__.__name__.replace('Agent', '').lower()
        description = f"Improve the {class_name} for {self.file_path.stem}"
        try:
            logging.info(f"Improving content with prompt: {prompt[:50]}...")

            # Add conversation context if available
            full_prompt = self._build_prompt_with_history(prompt)

            # Define backend callable for strategy
            def backend_callable(p: str, sp: Optional[str] = None, h: Optional[List[Dict[str, str]]] = None) -> str:
                return self.run_subagent(description, p, self.previous_content)

            # Execute strategy
            improvement = self.strategy.execute(
                prompt=full_prompt,
                context=self.previous_content,
                backend_call=backend_callable
            )

            # Apply post - processors
            for processor in self._post_processors:
                improvement = processor(improvement)

            # Score response quality
            quality = self._score_response_quality(improvement)

            # Retry if quality is poor
            if quality.value <= ResponseQuality.POOR.value and self._config.retry_count > 0:
                logging.warning(f"Response quality {quality.name}, retrying...")
                for _ in range(self._config.retry_count):
                    improvement = self.run_subagent(description, full_prompt, self.previous_content)
                    quality = self._score_response_quality(improvement)
                    if quality.value >= ResponseQuality.ACCEPTABLE.value:
                        break

            self.current_content = improvement

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
            return self.current_content
        except Exception as e:
            logging.warning(f"Failed to improve content: {e}")
            self.current_content = self.previous_content
            return self.current_content

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """Run a subagent using one of several AI backends.

        Delegates to agent_backend.run_subagent which selects the appropriate
        AI backend (copilot, GitHub Models, etc.) and executes the request.

        Args:
            description: Human - readable description of the task.
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
        result: str | None = agent_backend.run_subagent(description, prompt, original_content)
        if result is None:
            logging.warning("Subagent returned None, using fallback response")
            return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> dict[str, Any]:
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
        return agent_backend.get_backend_status()

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
        return agent_backend.describe_backends()

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot CLI is unavailable.

        Called when AI backend is not available. Override in subclasses to provide
        agent - specific fallback content.

        Returns:
            str: Fallback response text with helpful instructions.

        Note:
            Called automatically by run_subagent() when backend unavailable.
            Subclasses should override to provide domain - specific defaults.
        """
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub Copilot CLI ('copilot') not found or failed.\n"
            "# Install Copilot CLI: https://github.com / github / copilot - cli\n"
            "# Windows: winget install GitHub.Copilot\n"
            "# npm: npm install -g @github / copilot\n"
        )

    def update_file(self) -> bool:
        """Write the improved content back to the file.

        Writes current_content to disk, with special handling for markdown files
        which get normalized / fixed using the fix_markdown_content function.

        Returns:
            bool: True if the file was written successfully.

        Raises:
            OSError: If file write fails.

        Note:
            - Automatically detects markdown files (.md, .markdown, .plan.md)
            - Applies markdown normalization only to markdown files
            - Uses UTF - 8 encoding for all files
            - Creates parent directories if they don't exist

        Example:
            agent.current_content="# Improved Content"
            agent.update_file()  # Writes to agent.file_path
        """
        content_to_write = self.current_content
        # Only run the markdown fixer on markdown - like files. Applying markdown
        # normalization to source code can corrupt it.
        suffix = self.file_path.suffix.lower()
        is_markdown = suffix in {
            '.md', '.markdown'} or self.file_path.name.lower().endswith('.plan.md')
        if is_markdown:
            logging.debug(f"Applying markdown formatting to {self.file_path.name}")
            content_to_write = fix_markdown_content(content_to_write)

        logging.info(f"Writing {len(content_to_write)} bytes to {self.file_path.name}")
        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(content_to_write, encoding='utf-8')
        return True

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
        diff = difflib.unified_diff(
            self.previous_content.splitlines(keepends=True),
            self.current_content.splitlines(keepends=True),
            fromfile='previous',
            tofile='current'
        )
        diff_str = ''.join(diff)
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
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        prompt = template.template.format(**variables, content=self.previous_content)
        return self.improve_content(prompt)

    # ========== Conversation History ==========

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to conversation history.

        Args:
            role: Message role (user, assistant, system).
            content: Message content.
        """
        role_value = role.strip().lower()
        try:
            role_enum = MessageRole(role_value)
        except ValueError:
            role_enum = MessageRole.SYSTEM
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
        recent = self._conversation_history[-6:]  # Last 3 exchanges
        context_lines: list[str] = []
        for msg in recent:
            context_lines.append(f"[{msg.role}]: {msg.content[:200]}...")

        return f"Previous context:\n{''.join(context_lines)}\n\nCurrent request:\n{prompt}"

    # ========== Response Post - Processing ==========

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
        if not response or response.isspace():
            return ResponseQuality.INVALID

        # Basic quality heuristics
        score = 3  # Start at ACCEPTABLE

        # Longer responses generally better (to a point)
        if len(response) > 100:
            score += 1
        if len(response) < 20:
            score -= 1

        # Check for error indicators
        error_indicators = ["error", "failed", "unavailable", "unable"]
        if any(ind in response.lower() for ind in error_indicators):
            score -= 1

        # Check for actual content
        if response.strip().startswith("#") or "def " in response or "class " in response:
            score += 1

        return ResponseQuality(min(max(score, 1), 5))

    # ========== Cache Management ==========

    def _generate_cache_key(self, prompt: str, content: str) -> str:
        """Generate a content-based cache key.

        Args:
            prompt: The prompt.
            content: The content being processed.

        Returns:
            SHA256 hash key.
        """
        combined = f"{prompt}:{content}:{self._model or ''}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

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
        total_hits = sum(e.hit_count for e in cls._response_cache.values())
        avg_quality = sum(
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
        backend_status = cls.get_backend_status()
        backend_available = any(
            cast(dict[str, Any], v).get("available", False)
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
        state_path = path or self.file_path.with_suffix(".state.json")
        state: dict[str, Any] = {
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
        state_path = path or self.file_path.with_suffix(".state.json")
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
        # Rough estimate: ~4 characters per token
        return len(text) // 4

    def truncate_for_context(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit.

        Args:
            text: Text to truncate.
            max_tokens: Maximum tokens allowed.

        Returns:
            Truncated text with ellipsis if truncated.
        """
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars - 20] + "\n... [truncated]"


# ========== Session 8 Helper Classes ==========

class RequestBatcher:
    """Batch processor for multiple file requests.

    Handles efficient processing of multiple files in batches
    with priority - based ordering and parallel execution.

    Attributes:
        batch_size: Maximum requests per batch.
        max_concurrent: Maximum concurrent requests.
        queue: Pending batch requests.
        results: Completed batch results.

    Example:
        batcher=RequestBatcher(batch_size=10)
        batcher.add_request(BatchRequest(Path("file.py"), "Improve"))
        results=batcher.process_all(agent_factory)
    """

    def __init__(
        self,
        batch_size: int = 10,
        max_concurrent: int = 4
    ) -> None:
        """Initialize the request batcher.

        Args:
            batch_size: Maximum requests per batch.
            max_concurrent: Maximum concurrent requests.
        """
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.queue: List[BatchRequest] = []
        self.results: List[BatchResult] = []
        logging.debug(f"RequestBatcher initialized with batch_size={batch_size}")

    def add_request(self, request: BatchRequest) -> None:
        """Add a request to the queue.

        Args:
            request: The batch request to add.
        """
        self.queue.append(request)
        logging.debug(f"Added request for {request.file_path}")

    def add_requests(self, requests: List[BatchRequest]) -> None:
        """Add multiple requests to the queue.

        Args:
            requests: List of batch requests to add.
        """
        self.queue.extend(requests)
        logging.debug(f"Added {len(requests)} requests to queue")

    def get_queue_size(self) -> int:
        """Get the current queue size.

        Returns:
            Number of pending requests.
        """
        return len(self.queue)

    def clear_queue(self) -> None:
        """Clear all pending requests."""
        self.queue.clear()
        logging.debug("Request queue cleared")

    def _sort_by_priority(self) -> List[BatchRequest]:
        """Sort requests by priority (highest first).

        Returns:
            Sorted list of requests.
        """
        return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)

    def process_batch(
        self,
        agent_factory: Callable[[str], "BaseAgent"]
    ) -> List[BatchResult]:
        """Process a single batch of requests.

        Args:
            agent_factory: Factory function to create agents.

        Returns:
            List of batch results.
        """
        sorted_requests = self._sort_by_priority()
        batch = sorted_requests[:self.batch_size]
        results: List[BatchResult] = []

        for request in batch:
            start_time = time.time()
            try:
                agent = agent_factory(str(request.file_path))
                agent.read_previous_content()
                content = agent.improve_content(request.prompt)

                result = BatchResult(
                    file_path=request.file_path,
                    success=True,
                    content=content,
                    processing_time=time.time() - start_time
                )

                if request.callback:
                    request.callback(content)

            except Exception as e:
                result = BatchResult(
                    file_path=request.file_path,
                    success=False,
                    error=str(e),
                    processing_time=time.time() - start_time
                )

            results.append(result)
            self.queue.remove(request)

        self.results.extend(results)
        return results

    def process_all(
        self,
        agent_factory: Callable[[str], "BaseAgent"]
    ) -> List[BatchResult]:
        """Process all queued requests.

        Args:
            agent_factory: Factory function to create agents.

        Returns:
            List of all batch results.
        """
        all_results: List[BatchResult] = []
        while self.queue:
            batch_results = self.process_batch(agent_factory)
            all_results.extend(batch_results)
        return all_results

    def get_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics.

        Returns:
            Dictionary with processing stats.
        """
        if not self.results:
            return {"processed": 0, "success_rate": 0.0, "avg_time": 0.0}

        successful = sum(1 for r in self.results if r.success)
        total_time = sum(r.processing_time for r in self.results)

        return {
            "processed": len(self.results),
            "successful": successful,
            "failed": len(self.results) - successful,
            "success_rate": successful / len(self.results),
            "avg_time": total_time / len(self.results),
            "total_time": total_time,
        }


class AuthenticationManager:
    """Manager for authentication methods.

    Handles various authentication methods for AI backends
    including API keys, bearer tokens, OAuth2, and custom auth.

    Attributes:
        config: Authentication configuration.
        token_cache: Cached authentication tokens.

    Example:
        auth=AuthenticationManager(AuthConfig(method=AuthMethod.BEARER_TOKEN, token="xxx"))
        headers=auth.get_headers()
    """

    def __init__(self, config: Optional[AuthConfig] = None) -> None:
        """Initialize authentication manager.

        Args:
            config: Authentication configuration.
        """
        self.config = config or AuthConfig()
        self.token_cache: Dict[str, str] = {}
        logging.debug(f"AuthenticationManager initialized with method={self.config.method.value}")

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers.

        Returns:
            Dictionary of HTTP headers for authentication.
        """
        headers: Dict[str, str] = {}

        if self.config.method == AuthMethod.API_KEY:
            headers["X-API-Key"] = self.config.api_key
        elif self.config.method == AuthMethod.BEARER_TOKEN:
            headers["Authorization"] = f"Bearer {self.config.token}"
        elif self.config.method == AuthMethod.BASIC_AUTH:
            import base64
            credentials = f"{self.config.username}:{self.config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        elif self.config.method == AuthMethod.OAUTH2:
            token = self._get_oauth_token()
            headers["Authorization"] = f"Bearer {token}"

        # Add custom headers
        headers.update(self.config.custom_headers)

        return headers

    def _get_oauth_token(self) -> str:
        """Get OAuth2 token (with caching).

        Returns:
            OAuth2 access token.
        """
        cache_key = f"oauth_{self.config.oauth_client_id}"
        if cache_key in self.token_cache:
            return self.token_cache[cache_key]

        # In production, would exchange credentials for token
        # For now, return placeholder
        token = self.config.token or "oauth_token_placeholder"
        self.token_cache[cache_key] = token
        return token

    def refresh_token(self) -> None:
        """Refresh authentication token."""
        self.token_cache.clear()
        logging.debug("Authentication tokens refreshed")

    def set_custom_header(self, key: str, value: str) -> None:
        """Set a custom header.

        Args:
            key: Header name.
            value: Header value.
        """
        self.config.custom_headers[key] = value

    def validate(self) -> bool:
        """Validate authentication configuration.

        Returns:
            True if configuration is valid.
        """
        if self.config.method == AuthMethod.NONE:
            return True
        if self.config.method == AuthMethod.API_KEY:
            return bool(self.config.api_key)
        if self.config.method == AuthMethod.BEARER_TOKEN:
            return bool(self.config.token)
        if self.config.method == AuthMethod.BASIC_AUTH:
            return bool(self.config.username and self.config.password)
        if self.config.method == AuthMethod.OAUTH2:
            return bool(self.config.oauth_client_id and self.config.oauth_client_secret)
        return True


class PromptVersionManager:
    """Manager for prompt versioning and A/B testing.

    Supports both simple and advanced version management APIs.

    Attributes:
        versions: Registered prompt versions.
        active_version: Currently active version.
        metrics: Collected metrics per version.
    """

    def __init__(self) -> None:
        """Initialize the prompt version manager."""
        self.versions: Dict[str, PromptVersion] = {}
        self.active_version: Optional[str] = None
        self.metrics: Dict[str, Dict[str, float]] = {}
        self._old_api_versions: Dict[str, List[PromptVersion]] = {}  # For old API
        self.selection_history: List[Dict[str, Any]] = []
        logging.debug("PromptVersionManager initialized")

    def register_version(self, version: PromptVersion) -> None:
        """Register a prompt version (old API).

        Args:
            version: The prompt version to register.
        """
        # Old API: organize by template_id
        template_id = version.template_id
        if template_id not in self._old_api_versions:
            self._old_api_versions[template_id] = []
        self._old_api_versions[template_id].append(version)

        # Also store in new API format
        self.versions[version.version_id] = version
        if self.active_version is None:
            self.active_version = version.version_id
        logging.debug(f"Registered version {version.version_id} for {template_id}")

    def add_version(self, version: PromptVersion) -> None:
        """Add a prompt version (new API).

        Args:
            version: The prompt version to add.
        """
        self.versions[version.version] = version
        if self.active_version is None:
            self.active_version = version.version
        logging.debug(f"Added version {version.version}")

    def set_active(self, version: str) -> None:
        """Set the active version (new API).

        Args:
            version: Version identifier.
        """
        if version in self.versions:
            self.active_version = version
            self.versions[version].active = True
            logging.debug(f"Set active version to {version}")

    def get_active(self) -> Optional[PromptVersion]:
        """Get the active version (new API).

        Returns:
            The active prompt version.
        """
        if self.active_version and self.active_version in self.versions:
            return self.versions[self.active_version]
        return None

    def get_versions(self, template_id: str = "") -> List[PromptVersion]:
        """Get all versions (old API).

        Args:
            template_id: The template ID.

        Returns:
            List of prompt versions.
        """
        if template_id:
            return self._old_api_versions.get(template_id, [])
        return list(self.versions.values())

    def select_version(self, template_id: str = "") -> Optional[PromptVersion]:
        """Select a version using weighted random selection (old API).

        Args:
            template_id: The template ID.

        Returns:
            Selected prompt version.
        """
        import random

        versions = self.get_versions(template_id)
        if not versions:
            return None

        # Weighted selection
        total_weight = sum(v.weight for v in versions)
        if total_weight <= 0:
            return versions[0]

        r = random.uniform(0, total_weight)
        cumulative = 0.0
        for version in versions:
            cumulative += version.weight
            if r <= cumulative:
                self.selection_history.append({
                    "template_id": template_id,
                    "version_id": version.version_id,
                    "variant": version.variant,
                    "timestamp": time.time()
                })
                return version

        return versions[-1]

    def record_metric(
        self,
        version_id: str,
        metric_name: str,
        value: float
    ) -> None:
        """Record a metric for a version.

        Args:
            version_id: The version ID.
            metric_name: Name of the metric.
            value: Metric value.
        """
        if version_id not in self.metrics:
            self.metrics[version_id] = {}

        # Rolling average for old API
        if metric_name in self.metrics[version_id]:
            current = self.metrics[version_id][metric_name]
            self.metrics[version_id][metric_name] = (current + value) / 2
        else:
            self.metrics[version_id][metric_name] = value

        # Also update in version if it exists
        if version_id in self.versions:
            self.versions[version_id].metrics[metric_name] = value

    def get_best_version(
            self,
            template_id: str = "",
            metric: str = "quality") -> Optional[PromptVersion]:
        """Get the best performing version.

        Args:
            template_id: Optional template ID.
            metric: Metric to use for comparison.

        Returns:
            Best performing version.
        """
        versions = self.get_versions(template_id) if template_id else list(self.versions.values())
        if not versions:
            return None

        best: Optional[PromptVersion] = None
        best_score = -float('inf')

        for version in versions:
            score = version.metrics.get(metric, 0)
            if score > best_score:
                best_score = score
                best = version

        return best

    def generate_report(self, template_id: str = "") -> Dict[str, Any]:
        """Generate a report about versions.

        Args:
            template_id: Optional template ID.

        Returns:
            Report with version statistics.
        """
        report: Dict[str, Any] = {
            "total_versions": len(self.versions),
            "versions": {}
        }

        for version_id, version in self.versions.items():
            report["versions"][version_id] = {
                "content": version.content,
                "active": version.active,
                "metrics": version.metrics
            }

        return report

    def get_ab_report(self, template_id: str) -> Dict[str, Any]:
        """Get A/B testing report for a template (old API).

        Args:
            template_id: The template ID.

        Returns:
            Report with version statistics.
        """
        versions = self.get_versions(template_id)
        selections = [s for s in self.selection_history if s["template_id"] == template_id]

        report: Dict[str, Any] = {
            "template_id": template_id,
            "total_selections": len(selections),
            "versions": {}
        }

        for version in versions:
            version_selections = [s for s in selections if s["version_id"] == version.version_id]
            report["versions"][version.version_id] = {
                "variant": version.variant,
                "selections": len(version_selections),
                "metrics": self.metrics.get(version.version_id, {})
            }

        return report


class MultimodalProcessor:
    """Processor for multimodal inputs.

    Handles processing of various input types including
    text, images, diagrams, and code for AI backends.

    Attributes:
        inputs: List of multimodal inputs.
        processed: Processed content ready for AI.

    Example:
        processor=MultimodalProcessor()
        processor.add_input(MultimodalInput(InputType.TEXT, "Hello"))
        processor.add_input(MultimodalInput(InputType.IMAGE, base64_data))
        prompt=processor.build_prompt()
    """

    def __init__(self) -> None:
        """Initialize the multimodal processor."""
        self.inputs: List[MultimodalInput] = []
        self.processed: str = ""
        logging.debug("MultimodalProcessor initialized")

    def add_input(self, input_data: MultimodalInput) -> None:
        """Add a multimodal input.

        Args:
            input_data: The input to add.
        """
        self.inputs.append(input_data)
        logging.debug(f"Added {input_data.input_type.value} input")

    def add_text(self, text: str) -> None:
        """Add text input.

        Args:
            text: Text content.
        """
        self.add_input(MultimodalInput(InputType.TEXT, text))

    def add_image(self, data: str, mime_type: str = "image / png") -> None:
        """Add image input (base64 encoded).

        Args:
            data: Base64 encoded image data.
            mime_type: Image MIME type.
        """
        self.add_input(MultimodalInput(InputType.IMAGE, data, mime_type))

    def add_code(self, code: str, language: str = "python") -> None:
        """Add code input.

        Args:
            code: Source code.
            language: Programming language.
        """
        self.add_input(MultimodalInput(
            InputType.CODE,
            code,
            metadata={"language": language}
        ))

    def build_prompt(self) -> str:
        """Build combined prompt from all inputs.

        Returns:
            Combined prompt string.
        """
        parts: List[str] = []

        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                parts.append(inp.content)
            elif inp.input_type == InputType.CODE:
                lang = inp.metadata.get("language", "")
                parts.append(f"```{lang}\n{inp.content}\n```")
            elif inp.input_type == InputType.IMAGE:
                parts.append(f"[Image: {inp.mime_type}]")
            elif inp.input_type == InputType.DIAGRAM:
                parts.append(f"[Diagram: {inp.metadata.get('type', 'unknown')}]")

        self.processed = "\n\n".join(parts)
        return self.processed

    def get_api_messages(self) -> List[Dict[str, Any]]:
        """Get messages formatted for multimodal API.

        Returns:
            List of message dictionaries.
        """
        messages: List[Dict[str, Any]] = []

        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                messages.append({"type": "text", "text": inp.content})
            elif inp.input_type == InputType.IMAGE:
                messages.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{inp.mime_type};base64,{inp.content}"
                    }
                })
            elif inp.input_type == InputType.CODE:
                messages.append({
                    "type": "text",
                    "text": f"```{inp.metadata.get('language', '')}\n{inp.content}\n```"
                })

        return messages

    def clear(self) -> None:
        """Clear all inputs."""
        self.inputs.clear()
        self.processed = ""


class AgentComposer:
    """Composer for multi-agent workflows.

    Orchestrates multiple agents working together on a task,
    handling dependencies and result aggregation.

    Attributes:
        agents: Configured agents for composition.
        results: Results from each agent.
        execution_order: Calculated execution order.

    Example:
        composer=AgentComposer()
        composer.add_agent(ComposedAgent("coder", order=1))
        composer.add_agent(ComposedAgent("tests", order=2, depends_on=["coder"]))
        result=composer.execute(file_path, prompt)
    """

    def __init__(self) -> None:
        """Initialize the agent composer."""
        self.agents: List[ComposedAgent] = []
        self.results: Dict[str, str] = {}
        self.execution_order: List[str] = []
        logging.debug("AgentComposer initialized")

    def add_agent(self, agent: ComposedAgent) -> None:
        """Add an agent to the composition.

        Args:
            agent: The agent configuration to add.
        """
        self.agents.append(agent)
        self._calculate_execution_order()
        logging.debug(f"Added agent: {agent.agent_type}")

    def _calculate_execution_order(self) -> None:
        """Calculate execution order based on dependencies."""
        # Topological sort
        sorted_agents: List[str] = []
        visited: set[str] = set()
        temp: set[str] = set()

        def visit(agent_type: str) -> None:
            if agent_type in temp:
                raise ValueError(f"Circular dependency detected for {agent_type}")
            if agent_type in visited:
                return

            temp.add(agent_type)
            agent = next((a for a in self.agents if a.agent_type == agent_type), None)
            if agent:
                for dep in agent.depends_on:
                    visit(dep)
            temp.remove(agent_type)
            visited.add(agent_type)
            sorted_agents.append(agent_type)

        for agent in sorted(self.agents, key=lambda a: a.order):
            if agent.agent_type not in visited:
                visit(agent.agent_type)

        self.execution_order = sorted_agents

    def execute(
        self,
        file_path: str,
        prompt: str,
        agent_factory: Callable[[str, str], "BaseAgent"]
    ) -> Dict[str, str]:
        """Execute the composed agents.

        Args:
            file_path: Path to the file to process.
            prompt: Base prompt for agents.
            agent_factory: Factory to create agents (type, path).

        Returns:
            Dictionary of results from each agent.
        """
        self.results.clear()
        current_content = ""

        for agent_type in self.execution_order:
            agent_config = next((a for a in self.agents if a.agent_type == agent_type), None)
            if not agent_config:
                continue

            # Create agent
            agent = agent_factory(agent_type, file_path)

            # Build prompt with context from previous agents
            enhanced_prompt = prompt
            for dep in agent_config.depends_on:
                if dep in self.results:
                    enhanced_prompt += f"\n\nPrevious {dep} result:\n{self.results[dep][:500]}"

            # Process
            if current_content:
                agent.previous_content = current_content

            result = agent.improve_content(enhanced_prompt)
            self.results[agent_type] = result
            current_content = result

        return self.results

    def get_final_result(self) -> str:
        """Get the final aggregated result.

        Returns:
            Content from the last executed agent.
        """
        if not self.execution_order:
            return ""
        return self.results.get(self.execution_order[-1], "")


class SerializationManager:
    """Manager for custom serialization formats.

    Handles serialization and deserialization of agent data
    in various formats with optional compression and encryption.

    Attributes:
        config: Serialization configuration.

    Example:
        manager=SerializationManager(SerializationConfig(format=SerializationFormat.JSON))
        data=manager.serialize({"key": "value"})
        obj=manager.deserialize(data)
    """

    def __init__(self, config: Optional[SerializationConfig] = None) -> None:
        """Initialize serialization manager.

        Args:
            config: Serialization configuration.
        """
        self.config = config or SerializationConfig()
        logging.debug(f"SerializationManager initialized with format={self.config.format.value}")

    def serialize(self, data: Any) -> bytes:
        """Serialize data to bytes.

        Args:
            data: Data to serialize.

        Returns:
            Serialized bytes.
        """
        if self.config.format == SerializationFormat.JSON:
            result = json.dumps(data, indent=2).encode("utf-8")
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle
            result = pickle.dumps(data)
        else:
            # Default to JSON
            result = json.dumps(data).encode("utf-8")

        if self.config.compression:
            import zlib
            result = zlib.compress(result)

        return result

    def deserialize(self, data: bytes) -> Any:
        """Deserialize bytes to data.

        Args:
            data: Serialized bytes.

        Returns:
            Deserialized data.
        """
        if self.config.compression:
            import zlib
            data = zlib.decompress(data)

        if self.config.format == SerializationFormat.JSON:
            return json.loads(data.decode("utf-8"))
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle
            return pickle.loads(data)
        else:
            return json.loads(data.decode("utf-8"))

    def save_to_file(self, data: Any, path: Path) -> None:
        """Save serialized data to file.

        Args:
            data: Data to save.
            path: File path.
        """
        serialized = self.serialize(data)
        path.write_bytes(serialized)
        logging.debug(f"Saved {len(serialized)} bytes to {path}")

    def load_from_file(self, path: Path) -> Any:
        """Load data from file.

        Args:
            path: File path.

        Returns:
            Deserialized data.
        """
        data = path.read_bytes()
        return self.deserialize(data)


class FilePriorityManager:
    """Manager for file priority and request ordering.

    Determines file priority based on patterns, extensions,
    and custom rules for request prioritization.

    Attributes:
        config: Priority configuration.

    Example:
        manager=FilePriorityManager()
        manager.set_pattern_priority("*.py", FilePriority.HIGH)
        priority=manager.get_priority(Path("main.py"))
    """

    def __init__(self, config: Optional[FilePriorityConfig] = None) -> None:
        """Initialize priority manager.

        Args:
            config: Priority configuration.
        """
        self.config = config or FilePriorityConfig()
        # Default extension priorities
        self._default_extensions = {
            ".py": FilePriority.HIGH,
            ".js": FilePriority.HIGH,
            ".ts": FilePriority.HIGH,
            ".md": FilePriority.NORMAL,
            ".json": FilePriority.LOW,
            ".txt": FilePriority.LOW,
        }
        logging.debug("FilePriorityManager initialized")

    def set_pattern_priority(self, pattern: str, priority: FilePriority) -> None:
        """Set priority for a path pattern.

        Args:
            pattern: Glob pattern.
            priority: Priority level.
        """
        self.config.path_patterns[pattern] = priority

    def set_extension_priority(self, extension: str, priority: FilePriority) -> None:
        """Set priority for a file extension.

        Args:
            extension: File extension (with dot).
            priority: Priority level.
        """
        self.config.extension_priorities[extension] = priority

    def get_priority(self, path: Path) -> FilePriority:
        """Get priority for a file.

        Args:
            path: File path.

        Returns:
            Priority level.
        """
        # Check path patterns first
        import fnmatch
        path_str = str(path)
        for pattern, priority in self.config.path_patterns.items():
            if fnmatch.fnmatch(path_str, pattern):
                return priority

        # Check extension
        ext = path.suffix.lower()
        if ext in self.config.extension_priorities:
            return self.config.extension_priorities[ext]
        if ext in self._default_extensions:
            return self._default_extensions[ext]

        return self.config.default_priority

    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
        """Sort paths by priority (highest first).

        Args:
            paths: List of file paths.

        Returns:
            Sorted list of paths.
        """
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)

    def filter_by_priority(
        self,
        paths: List[Path],
        min_priority: FilePriority = FilePriority.LOW
    ) -> List[Path]:
        """Filter paths by minimum priority.

        Args:
            paths: List of file paths.
            min_priority: Minimum priority to include.

        Returns:
            Filtered list of paths.
        """
        return [p for p in paths if self.get_priority(p).value >= min_priority.value]


# ========== Context Window Management ==========

@dataclass
class ContextWindow:
    """Manages token-based context window."""
    max_tokens: int
    messages: List[str] = field(default_factory=_empty_list_str)
    token_counts: List[int] = field(default_factory=_empty_list_int)

    @property
    def used_tokens(self) -> int:
        """Get total used tokens."""
        return sum(self.token_counts)

    @property
    def available_tokens(self) -> int:
        """Get available tokens."""
        return max(0, self.max_tokens - self.used_tokens)

    def add(self, message: str, token_count: int) -> None:
        """Add a message to the window."""
        self.messages.append(message)
        self.token_counts.append(token_count)

        # Truncate if necessary
        while self.used_tokens > self.max_tokens and self.messages:
            self.messages.pop(0)
            self.token_counts.pop(0)

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()
        self.token_counts.clear()


# ========== Multimodal Builder ==========

@dataclass
class MultimodalBuilder:
    """Builds multimodal input sets."""
    inputs: List[MultimodalInput] = field(default_factory=lambda: cast(List[MultimodalInput], []))

    def add(self, content: str, input_type: "InputType") -> None:
        """Add an input."""
        self.inputs.append(MultimodalInput(content=content, input_type=input_type))

    def add_text(self, content: str) -> None:
        """Add text input."""
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.TEXT))

    def add_image(self, content: str) -> None:
        """Add image input."""
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.IMAGE))

    def build(self) -> List[MultimodalInput]:
        """Build and return inputs."""
        return self.inputs


# ========== Response Caching ==========
@dataclass
class ResponseCache:
    """Caches responses based on prompts."""
    cache_dir: Path
    cache_data: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def __post_init__(self) -> None:
        """Initialize cache directory."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt."""
        return hashlib.md5(prompt.encode()).hexdigest()

    def set(self, prompt: str, response: str) -> None:
        """Cache a response."""
        key = self._get_cache_key(prompt)
        self.cache_data[key] = response

        # Also write to disk
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps({"prompt": prompt, "response": response}))

    def get(self, prompt: str) -> Optional[str]:
        """Get cached response."""
        key = self._get_cache_key(prompt)
        if key in self.cache_data:
            return self.cache_data[key]

        # Try to load from disk
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            self.cache_data[key] = data["response"]
            return data["response"]

        return None

    def invalidate(self, prompt: str) -> None:
        """Invalidate cached response."""
        key = self._get_cache_key(prompt)
        self.cache_data.pop(key, None)

        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()


# ========== Agent Composition Patterns ==========

@dataclass
class AgentPipeline:
    """Chains agent steps sequentially."""
    steps: Dict[str, Callable[[Any], Any]] = field(default_factory=_empty_dict_str_callable_any_any)
    step_order: List[str] = field(default_factory=_empty_list_str)

    def add_step(self, name: str, func: Callable[[Any], Any]) -> None:
        """Add a pipeline step."""
        self.steps[name] = func
        self.step_order.append(name)

    def execute(self, data: Any) -> Any:
        """Execute pipeline."""
        result = data
        for step_name in self.step_order:
            result = self.steps[step_name](result)
        return result


@dataclass
class AgentParallel:
    """Executes agent branches in parallel conceptually."""
    branches: Dict[str, Callable[[Any], Any]] = field(default_factory=_empty_dict_str_callable_any_any)

    def add_branch(self, name: str, func: Callable[[Any], Any]) -> None:
        """Add a parallel branch."""
        self.branches[name] = func

    def execute(self, data: Any) -> Dict[str, Any]:
        """Execute all branches."""
        return {name: func(data) for name, func in self.branches.items()}


@dataclass
class AgentRouter:
    """Routes input based on conditions."""
    routes: List[tuple[Callable[[Any], bool], Callable[[Any], Any]]] = field(default_factory=_empty_routes_list)
    default_handler: Optional[Callable[[Any], Any]] = None

    def add_route(self, condition: Callable[[Any], bool], handler: Callable[[Any], Any]) -> None:
        """Add a route."""
        self.routes.append((condition, handler))

    def set_default(self, handler: Callable[[Any], Any]) -> None:
        """Set default handler."""
        self.default_handler = handler

    def route(self, data: Any) -> Any:
        """Route and execute."""
        for condition, handler in self.routes:
            if condition(data):
                return handler(data)

        if self.default_handler:
            return self.default_handler(data)

        return data


# ========== Token Budget ==========

@dataclass
class TokenBudget:
    """Manages token allocation."""
    total: int
    allocations: Dict[str, int] = field(default_factory=_empty_dict_str_int)

    @property
    def used(self) -> int:
        """Get total used tokens."""
        return sum(self.allocations.values())

    @property
    def remaining(self) -> int:
        """Get remaining tokens."""
        return max(0, self.total - self.used)

    def allocate(self, name: str, tokens: int) -> None:
        """Allocate tokens."""
        # Cap allocation to not exceed total
        capped = min(tokens, self.total - sum(v for k, v in self.allocations.items() if k != name))
        self.allocations[name] = max(0, capped)

    def release(self, name: str) -> None:
        """Release allocated tokens."""
        self.allocations.pop(name, None)


# ========== State Persistence ==========

@dataclass
class StatePersistence:
    """Persists agent state to disk."""
    state_file: Path
    backup: bool = False
    backup_count: int = 0

    def save(self, state: Dict[str, Any]) -> None:
        """Save state to file."""
        if self.backup and self.state_file.exists():
            backup_file = self.state_file.parent / f"{self.state_file.stem}.{self.backup_count}.bak"
            self.state_file.rename(backup_file)
            self.backup_count += 1

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state))

    def load(self, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Load state from file."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())

        return default or {}


# ========== Model Configuration & Selection ==========

@dataclass
class ModelConfig:
    """Model configuration."""
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class ModelSelector:
    """Selects models for different agent types."""
    models: Dict[str, ModelConfig] = field(default_factory=_empty_dict_str_modelconfig)

    def __post_init__(self) -> None:
        """Initialize with default model."""
        if "default" not in self.models:
            self.models["default"] = ModelConfig(model_id="gpt-3.5-turbo")

    def select(self, agent_type: str) -> ModelConfig:
        """Select model for agent type."""
        selected = self.models.get(agent_type)
        if selected is not None:
            return selected
        return self.models["default"]

    def set_model(self, agent_type: str, config: ModelConfig) -> None:
        """Set model for agent type."""
        self.models[agent_type] = config


# ========== Authentication Management ==========

@dataclass
class AuthManager:
    """Manages authentication."""
    method: AuthMethod | str | None = None
    credentials: Dict[str, str] = field(default_factory=_empty_dict_str_str)
    custom_headers: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def set_method(self, method: str, **kwargs: str) -> None:
        """Set authentication method."""
        self.method = method
        self.credentials = kwargs

    def add_custom_header(self, header: str, value: str) -> None:
        """Add custom header."""
        self.custom_headers[header] = value

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        headers = dict(self.custom_headers)

        # Convert enum to string if needed
        method = self.method
        if isinstance(method, AuthMethod):
            method = method.value

        if method == "api_key" and "api_key" in self.credentials:
            headers["X-API-Key"] = self.credentials["api_key"]
        elif method == "token" and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"
        elif method == "bearer_token" and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"

        return headers


# ========== Quality Scoring ==========

@dataclass
class QualityScorer:
    """Scores response quality."""
    criteria: Dict[str, tuple[Callable[[str], float], float]] = field(default_factory=_empty_dict_str_quality_criteria)

    def add_criterion(self, name: str, func: Callable[[str], float], weight: float = 1.0) -> None:
        """Add scoring criterion."""
        self.criteria[name] = (func, weight)

    def score(self, text: str) -> float:
        """Score response quality."""
        if not self.criteria:
            # Default: score based on length
            length_score = min(1.0, len(text) / 200.0)
            return length_score

        total_weight = 0.0
        total_score = 0.0

        for func, weight in self.criteria.values():
            score = func(text)
            total_score += score * weight
            total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0


# ========== A/B Testing ==========

@dataclass
class ABTest:
    """A/B test for variants."""
    name: str
    variants: List[str]
    weights: List[float] = field(default_factory=_empty_list_float)
    variant_counts: Dict[str, int] = field(default_factory=_empty_dict_str_int)

    def __post_init__(self) -> None:
        """Initialize variant counts."""
        for variant in self.variants:
            self.variant_counts[variant] = 0

        # Normalize weights if not provided
        if not self.weights:
            self.weights = [1.0 / len(self.variants)] * len(self.variants)

    def select_variant(self) -> str:
        """Select a variant based on weights."""
        import random
        return random.choices(self.variants, weights=self.weights, k=1)[0]


# ========== Event Management ==========

class AgentEvent(Enum):
    """Agent event types."""
    START = "start"
    COMPLETE = "complete"
    ERROR = "error"


def _empty_agent_event_handlers() -> dict[AgentEvent, list[Callable[..., None]]]:
    return {}


@dataclass
class EventManager:
    """Manages agent events."""
    handlers: Dict[AgentEvent, List[Callable[..., None]]] = field(default_factory=_empty_agent_event_handlers)

    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        """Register event handler."""
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def emit(self, event: AgentEvent, data: Any = None) -> None:
        """Emit event."""
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()


# ========== Plugin Management ==========

@dataclass
class PluginManager:
    """Manages agent plugins."""
    plugins: Dict[str, Any] = field(default_factory=_empty_dict_str_any)

    def register(self, plugin: Any) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin

    def activate_all(self) -> None:
        """Activate all plugins."""
        for plugin in self.plugins.values():
            if hasattr(plugin, 'activate'):
                plugin.activate()

    def deactivate(self, name: str) -> None:
        """Deactivate a plugin."""
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, 'deactivate'):
                plugin.deactivate()


# ========== Health Checking ==========

@dataclass
class HealthChecker:
    """Checks agent health status."""
    checks: Dict[str, Callable[[], Dict[str, Any]]] = field(default_factory=_empty_dict_str_health_checks)
    request_count: int = 0
    error_count: int = 0
    total_latency: int = 0

    def add_check(self, name: str, check_func: Callable[[], Dict[str, Any]]) -> None:
        """Add a health check."""
        self.checks[name] = check_func

    def check(self) -> Dict[str, Any]:
        """Run health check."""
        components: dict[str, Any] = {}
        result: dict[str, Any] = {"status": "healthy", "components": components}

        for name, check_func in self.checks.items():
            components[name] = check_func()

        return result

    def record_request(self, success: bool, latency_ms: int) -> None:
        """Record a request."""
        self.request_count += 1
        self.total_latency += latency_ms
        if not success:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get health metrics."""
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0

        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "avg_latency_ms": avg_latency
        }


# ========== Configuration Profiles ==========

@dataclass
class ConfigProfile:
    """Configuration profile."""
    name: str
    settings: Dict[str, Any]
    parent: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        return self.settings.get(key, default)


@dataclass
class ProfileManager:
    """Manages configuration profiles."""
    profiles: Dict[str, ConfigProfile] = field(default_factory=_empty_dict_str_configprofile)
    active_name: Optional[str] = None

    @property
    def active(self) -> Optional[ConfigProfile]:
        """Get active profile."""
        if self.active_name and self.active_name in self.profiles:
            return self.profiles[self.active_name]
        return None

    def add_profile(self, profile: ConfigProfile) -> None:
        """Add a profile."""
        self.profiles[profile.name] = profile

    def set_active(self, name: str) -> None:
        """Set active profile."""
        if name in self.profiles:
            self.active_name = name

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting from active profile with inheritance."""
        if not self.active:
            return default

        # Check active profile
        if key in self.active.settings:
            return self.active.settings[key]

        # Check parent
        if self.active.parent and self.active.parent in self.profiles:
            parent = self.profiles[self.active.parent]
            if key in parent.settings:
                return parent.settings[key]

        return default


# Initialize default templates
for template in DEFAULT_PROMPT_TEMPLATES:
    BaseAgent.register_template(template)


def create_main_function(
    agent_class: Type[BaseAgent],
    description: str,
    context_help: str) -> Callable[[],
                                   None]:
    """Create a main function for an agent class."""
    def main() -> None:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '--describe-backends',
            action='store_true',
            help='Print which AI backends are available / configured and exit',
        )
        parser.add_argument(
            '--backend',
            choices=['auto', 'copilot', 'gh', 'github-models'],
            default=None,
            help='Select backend (overrides DV_AGENT_BACKEND for this run only)',
        )
        parser.add_argument(
            '--strategy',
            choices=['direct', 'cot', 'reflexion'],
            default='direct',
            help='Select reasoning strategy (direct, cot, reflexion)',
        )
        parser.add_argument(
            '--verbose',
            '-v',
            action='count',
            default=0,
            help='Increase verbosity (can be used multiple times, e.g. -vv)',
        )
        parser.add_argument('--context', required=True, help=context_help)
        parser.add_argument('--prompt', required=True, help='Prompt for improving the content')
        args = parser.parse_args()
        setup_logging(args.verbose)
        if args.backend:
            os.environ['DV_AGENT_BACKEND'] = args.backend
        if args.describe_backends:
            print(agent_class.describe_backends())
            return
        agent = agent_class(args.context)
        
        # Set strategy based on argument
        if args.strategy == 'cot':
            agent.set_strategy(agent_strategies.ChainOfThoughtStrategy())
        elif args.strategy == 'reflexion':
            agent.set_strategy(agent_strategies.ReflexionStrategy())
        else:
            agent.set_strategy(agent_strategies.DirectStrategy())
            
        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()
        if diff:
            logging.info(f"{agent_class.__name__.replace('Agent', '').lower()} updated:")
            logging.info(diff)
        else:
            logging.info(f"No changes made to {agent_class.__name__.replace('Agent', '').lower()}.")
    return main
