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

"""Models for agent communication, prompts, and tracing."""

from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from collections.abc import Callable
from .CoreEnums import MessageRole, FilePriority, InputType
from .BaseModels import _empty_list_str, _empty_list_dict_str_any, _empty_dict_str_any


@dataclass(slots=True)
class CascadeContext:
    """
    Context for recursive agent delegation (Phase 259/275).
    Tracks depth and lineage to prevent infinite loops and provide tracing.
    """

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    root_task_id: str | None = None

    parent_agent_id: str | None = None

    cascade_depth: int = 0
    max_depth: int = 10

    def next_level(self, agent_id: str) -> CascadeContext:
        """Create a child context for the next level of delegation."""
        return CascadeContext(
            task_id=str(uuid.uuid4()),
            correlation_id=self.correlation_id,
            root_task_id=self.root_task_id or self.task_id,
            parent_agent_id=agent_id,
            cascade_depth=self.cascade_depth + 1,
            max_depth=self.max_depth,
        )

    def is_bursting(self) -> bool:
        """Check if recursion depth limit reached."""
        return self.cascade_depth >= self.max_depth


@dataclass(slots=True)
class PromptTemplate:
    """reusable prompt template."""

    name: str

    template: str
    variables: list[str] = field(default_factory=_empty_list_str)
    id: str = ""
    description: str = ""
    version: str = "1.0"
    tags: list[str] = field(default_factory=_empty_list_str)

    def render(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)


@dataclass(slots=True)
class ConversationMessage:
    """A message in conversation history."""

    role: MessageRole

    content: str
    timestamp: float = field(default_factory=time.time)


class ConversationHistory:
    """Manages a conversation history with message storage and retrieval."""

    def __init__(self, max_messages: int = 100) -> None:
        self.messages: list[ConversationMessage] = []
        self.max_messages = max_messages

    def add(self, role: MessageRole, content: str) -> None:
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get_context(self) -> list[ConversationMessage]:
        return self.messages.copy()

    def clear(self) -> None:
        self.messages.clear()


class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        self.templates: dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        template = self.templates[template_name]
        return template.render(**kwargs)


class ResponsePostProcessor:
    """Manages post-processing hooks for agent responses."""

    def __init__(self) -> None:
        self.hooks: list[tuple[Callable[[str], str], int]] = []

    def register(self, hook: Callable[[str], str], priority: int = 0) -> None:
        self.hooks.append((hook, priority))

    def process(self, text: str) -> str:
        sorted_hooks = sorted(self.hooks, key=lambda x: x[1], reverse=True)
        for hook, _ in sorted_hooks:
            text = hook(text)

        return text


@dataclass(slots=True)
class PromptVersion:
    """Versioned prompt for A/B testing."""

    version: str
    content: str
    description: str = ""

    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metrics: dict[str, float] = field(default_factory=_empty_dict_str_any)

    # Old API compatibility fields (initialized in __init__)
    version_id: str = ""
    template_id: str = ""

    variant: str = ""
    prompt_text: str = ""
    weight: float = 1.0

    def __init__(
        self,
        version: str | None = None,
        content: str | None = None,
        description: str = "",
        active: bool = True,
        version_id: str | None = None,
        template_id: str | None = None,
        variant: str | None = None,
        prompt_text: str | None = None,
        weight: float = 1.0,
    ) -> None:
        self.version = version or version_id or ""
        self.content = content or prompt_text or ""

        self.description = description
        self.active = active
        self.created_at = datetime.now()
        self.metrics = {}
        self.version_id = self.version

        self.template_id = template_id or ""
        self.variant = variant or ""

        self.prompt_text = self.content
        self.weight = weight


class BatchRequest:
    """Request in a batch processing queue."""

    def __init__(
        self,
        file_path: Path | None = None,
        prompt: str | None = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Callable[[str], None] | None = None,
        max_size: int | None = None,
    ) -> None:
        self.file_path = file_path
        self.prompt = prompt or ""
        self.priority = priority
        self.callback = callback
        self.max_size = max_size
        self.items: list[Any] = []

    def add(self, item: Any) -> None:
        if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        return len(self.items)

    def execute(self, processor: Callable[[list[Any]], list[Any]]) -> list[Any]:
        return processor(self.items)


@dataclass(slots=True)
class BatchResult:
    """Result of a batch processing request."""

    file_path: Path | None
    success: bool
    content: str = ""
    error: str = ""
    processing_time: float = 0.0


@dataclass(slots=True)
class MultimodalInput:
    """Multimodal input for agents."""

    input_type: InputType
    content: str
    mime_type: str = ""
    metadata: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class ContextWindow:
    """Manages token-based context window."""

    max_tokens: int
    messages: list[str] = field(default_factory=_empty_list_str)
    token_counts: list[int] = field(default_factory=list)

    @property
    def used_tokens(self) -> int:
        return sum(self.token_counts)

    @property
    def available_tokens(self) -> int:
        return max(0, self.max_tokens - self.used_tokens)

    def add(self, message: str, token_count: int) -> None:
        self.messages.append(message)
        self.token_counts.append(token_count)
        while self.used_tokens > self.max_tokens and self.messages:
            self.messages.pop(0)
            self.token_counts.pop(0)

    def clear(self) -> None:
        self.messages.clear()
        self.token_counts.clear()


@dataclass(slots=True)
class MultimodalBuilder:
    """Builds multimodal input sets."""

    inputs: list[MultimodalInput] = field(default_factory=list)

    def add(self, content: str, input_type: InputType) -> None:
        self.inputs.append(MultimodalInput(content=content, input_type=input_type))

    def add_text(self, content: str) -> None:
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.TEXT))

    def add_image(self, content: str) -> None:
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.IMAGE))

    def build(self) -> list[MultimodalInput]:
        return self.inputs


@dataclass(slots=True)
class CachedResult:
    """A cached agent result."""

    file_path: str
    agent_name: str
    content_hash: str
    result: Any
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: int = 3600


@dataclass(slots=True)
class TelemetrySpan:
    """A telemetry span for tracing."""

    name: str
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    parent_id: str | None = None
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    events: list[dict[str, Any]] = field(default_factory=_empty_list_dict_str_any)


class SpanContext:
    """Context for a telemetry span."""

    def __init__(self, span: TelemetrySpan) -> None:
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        self._span.attributes[key] = value

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        self._span.events.append(
            {
                "name": name,
                "timestamp": time.time(),
                "attributes": attributes or {},
            }
        )
