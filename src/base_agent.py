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
Base Agent: Common functionality for all AI - powered agents.

Provides shared functionality for agents that improve code files using AI assistance.
"""

import argparse
import difflib
import json
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import sys
from typing import Optional, Dict, List, Any, Callable, Type
import hashlib
import time

try:
    from scripts.agent import agent_backend
except ImportError:
    # Fallback for when running directly or in tests without package structure
    try:
        import agent_backend  # type: ignore
    except ImportError:
        # Last resort: try to find it relative to this file
        sys.path.append(str(Path(__file__).parent))
        import agent_backend  # type: ignore

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]


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


# ========== Dataclasses for Data Structures ==========

@dataclass
class PromptTemplate:
    """Reusable prompt template.

    Attributes:
        id: Unique identifier for the template.
        name: Human - readable template name.
        template: The prompt template with {placeholders}.
        description: Description of when to use this template.
        version: Version string for A / B testing.
        tags: Tags for categorization.
    """
    id: str
    name: str
    template: str
    description: str = ""
    version: str = "1.0"
    tags: List[str] = field(default_factory=list)


@dataclass
class ConversationMessage:
    """A message in conversation history.

    Attributes:
        role: The role (user, assistant, system).
        content: Message content.
        timestamp: When the message was created.
    """
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: float = field(default_factory=time.time)


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
    details: Dict[str, Any] = field(default_factory=dict)


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
    custom_headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchRequest:
    """Request in a batch processing queue.

    Attributes:
        file_path: Path to the file to process.
        prompt: Improvement prompt.
        priority: Processing priority.
        callback: Optional callback on completion.
    """
    file_path: Path
    prompt: str
    priority: FilePriority = FilePriority.NORMAL
    callback: Optional[Callable[[str], None]] = None


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
    file_path: Path
    success: bool
    content: str = ""
    error: str = ""
    processing_time: float = 0.0


@dataclass
class PromptVersion:
    """Versioned prompt for A / B testing.

    Attributes:
        version_id: Unique version identifier.
        template_id: Reference to base template.
        variant: Variant name (A, B, control, etc.).
        prompt_text: The prompt text for this version.
        weight: Selection weight for A / B testing.
        metrics: Recorded metrics for this version.
    """
    version_id: str
    template_id: str
    variant: str
    prompt_text: str
    weight: float = 1.0
    metrics: Dict[str, float] = field(default_factory=dict)


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
    metadata: Dict[str, Any] = field(default_factory=dict)


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
    config: Dict[str, Any] = field(default_factory=dict)
    order: int = 0
    depends_on: List[str] = field(default_factory=list)


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
    options: Dict[str, Any] = field(default_factory=dict)
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
    path_patterns: Dict[str, FilePriority] = field(default_factory=dict)
    extension_priorities: Dict[str, FilePriority] = field(default_factory=dict)
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
    _event_hooks: Dict[EventType, List[Callable]] = {e: [] for e in EventType}

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

    def __enter__(self):
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug(f"{self.__class__.__name__} entering context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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

            improvement = self.run_subagent(description, full_prompt, self.previous_content)

            # Apply post - processors
            for processor in self._post_processors:
                improvement = processor(improvement)

            # Score response quality
            quality = self._score_response_quality(improvement)

            # Retry if quality is poor
            if quality.value <= ResponseQuality.POOR.value and self._config.retry_count > 0:
                logging.warning(f"Response quality {quality.name}, retrying...")
                for attempt in range(self._config.retry_count):
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
            self._conversation_history.append(ConversationMessage(role="user", content=prompt))
            self._conversation_history.append(ConversationMessage(
                role="assistant", content=improvement[:500]))

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
        result = agent_backend.run_subagent(description, prompt, original_content)
        if result is None:
            logging.warning("Subagent returned None, using fallback response")
            return original_content or self._get_fallback_response()
        return result

    @staticmethod
    def get_backend_status() -> dict:
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

    def update_file(self) -> None:
        """Write the improved content back to the file.

        Writes current_content to disk, with special handling for markdown files
        which get normalized / fixed using the fix_markdown_content function.

        Returns:
            None.

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
        self._conversation_history.append(ConversationMessage(role=role, content=content))

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
        context_lines = []
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
        return {"entries": len(cls._response_cache), "total_hits": total_hits, "avg_quality": sum(
            e.quality_score for e in cls._response_cache.values()) / max(len(cls._response_cache), 1)}

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
    def register_hook(cls, event: EventType, callback: Callable[[Dict[str, Any]], None]) -> None:
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
    def unregister_hook(cls, event: EventType, callback: Callable) -> None:
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
        backend_available = any(v.get("available", False)
                                for v in backend_status.values() if isinstance(v, dict))

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
        state = {
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
    """Manager for prompt versioning and A / B testing.

    Handles prompt version management, variant selection,
    and metrics tracking for A / B testing.

    Attributes:
        versions: Registered prompt versions.
        metrics: Collected metrics per version.
        selection_history: History of version selections.

    Example:
        manager=PromptVersionManager()
        manager.register_version(PromptVersion("v1", "improve", "A", "Improve {content}"))
        selected=manager.select_version("improve")
    """

    def __init__(self) -> None:
        """Initialize the prompt version manager."""
        self.versions: Dict[str, List[PromptVersion]] = {}
        self.metrics: Dict[str, Dict[str, float]] = {}
        self.selection_history: List[Dict[str, Any]] = []
        logging.debug("PromptVersionManager initialized")

    def register_version(self, version: PromptVersion) -> None:
        """Register a prompt version.

        Args:
            version: The prompt version to register.
        """
        if version.template_id not in self.versions:
            self.versions[version.template_id] = []
        self.versions[version.template_id].append(version)
        logging.debug(f"Registered version {version.version_id} for {version.template_id}")

    def get_versions(self, template_id: str) -> List[PromptVersion]:
        """Get all versions for a template.

        Args:
            template_id: The template ID.

        Returns:
            List of prompt versions.
        """
        return self.versions.get(template_id, [])

    def select_version(self, template_id: str) -> Optional[PromptVersion]:
        """Select a version using weighted random selection.

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
        r = random.uniform(0, total_weight)

        cumulative = 0
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

        # Rolling average
        current = self.metrics[version_id].get(metric_name, value)
        self.metrics[version_id][metric_name] = (current + value) / 2

    def get_best_version(
            self,
            template_id: str,
            metric: str = "quality") -> Optional[PromptVersion]:
        """Get the best performing version.

        Args:
            template_id: The template ID.
            metric: Metric to use for comparison.

        Returns:
            Best performing version.
        """
        versions = self.get_versions(template_id)
        if not versions:
            return None

        best: Optional[PromptVersion] = None
        best_score = -1.0

        for version in versions:
            score = self.metrics.get(version.version_id, {}).get(metric, 0)
            if score > best_score:
                best_score = score
                best = version

        return best or versions[0]

    def get_ab_report(self, template_id: str) -> Dict[str, Any]:
        """Get A / B testing report for a template.

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
        visited: set = set()
        temp: set = set()

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
