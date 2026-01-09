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

"""Data models and structures for BaseAgent."""

import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ========== Enums ==========

class AgentState(Enum):
    """Agent lifecycle states."""
    INITIALIZED = "initialized"
    IDLE = "idle"
    READING = "reading"
    PROCESSING = "processing"
    THINKING = "thinking"
    SIMULATING = "simulating"
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


class MessageRole(Enum):
    """Roles for conversation messages."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AgentEvent(Enum):
    """Agent event types."""
    START = "start"
    COMPLETE = "complete"
    ERROR = "error"


# ========== Utility Functions ==========

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


def _empty_agent_event_handlers() -> dict[AgentEvent, list[Callable[..., None]]]:
    return {}


# ========== Dataclasses ==========

@dataclass
class PromptTemplate:
    """Reusable prompt template.

    Attributes:
        name: Human-readable template name.
        template: The prompt template with {placeholders}.
        variables: List of variable names in the template.
        id: Optional unique identifier for the template.
        description: Description of when to use this template.
        version: Version string for A/B testing.
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
class CacheEntry:
    """Cached response entry.

    Attributes:
        key: Content-based cache key.
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
        model: Model name/ID for the backend.
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
        token: Bearer token for token-based auth.
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
        config: Agent-specific configuration.
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
        options: Format-specific options.
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


@dataclass
class MultimodalBuilder:
    """Builds multimodal input sets."""
    inputs: List[MultimodalInput] = field(default_factory=list)

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


@dataclass
class ModelConfig:
    """Model configuration."""
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class ConfigProfile:
    """Configuration profile."""
    name: str
    settings: Dict[str, Any]
    parent: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        return self.settings.get(key, default)


EventHook = Callable[[dict[str, Any]], None]
