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
Module: communication_models
Defines context lineage and communication models for agent task attribution.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .base_models import _empty_dict_str_any, _empty_list_dict_str_any, _empty_list_str
from .core_enums import FilePriority, InputType, MessageRole


@dataclass(slots=True)
class WorkState:
    """Mutable storage regarding intermediate results in a multi-agent pipeline."""
    results: dict[str, Any] = field(default_factory=dict)
    shared_data: dict[str, Any] = field(default_factory=dict)
    artifacts: list[Path] = field(default_factory=list)

    def update(self, key: str, value: Any) -> None:
        """Updates a result key regarding the current pipeline state."""
        self.results[key] = value

    def add_artifact(self, path: Path) -> None:
        """Records a new artifact path regarding the pipeline output."""
        if path not in self.artifacts:
            self.artifacts.append(path)


@dataclass(slots=True)
class CascadeContext:
    """Context for tracking cascade operations and preventing infinite recursion."""

    task_id: str = ""
<<<<<<< HEAD
    agent_id: str = ""
=======
    # Backwards-compatible alias: some callers pass `agent_id` as the task identifier
    agent_id: str = ""
    # Optional workflow identifier for tracking across systems
>>>>>>> copilot/sub-pr-29
    workflow_id: str = ""
    cascade_depth: int = 0
    depth_limit: int = 10
    tenant_id: str = ""
    security_scope: list[str] = field(default_factory=_empty_list_str)
    failure_history: list[dict[str, Any]] = field(default_factory=_empty_list_dict_str_any)

    def __post_init__(self) -> None:
        """Validate and normalize failure history after initialization functionally."""
        # Backwards compatibility: if agent_id provided and task_id not set, use agent_id
        if getattr(self, "agent_id", "") and not self.task_id:
            self.task_id = self.agent_id
        # Backwards compatibility: if workflow_id provided and task_id not set, use workflow_id
        elif getattr(self, "workflow_id", "") and not self.task_id:
            self.task_id = self.workflow_id
        if self.cascade_depth >= self.depth_limit:
            raise RecursionError(f"Recursion depth limit ({self.depth_limit}) exceeded at depth {self.cascade_depth}")

        if self.failure_history:
            def _normalize(item: Any) -> dict[str, Any] | None:
                if not isinstance(item, dict):
                    return None
                norm = item.copy()
                if "error" not in norm:
                    norm["error"] = "Unknown Error (Schema Violation)"
                if "timestamp" not in norm:
                    norm["timestamp"] = time.time()
                if "failure_type" not in norm:
                    norm["failure_type"] = "unknown"
                return norm

            # Filter and normalize regarding schema integrity
            self.failure_history = list(filter(None, map(_normalize, self.failure_history)))

    def next_level(self, child_task_id: str = "", agent_id: str = "") -> 'CascadeContext':
        """Create a child context at the next cascade level."""
        # Support both child_task_id and agent_id for backwards compatibility
        task_id = child_task_id or agent_id

        if self.is_bursting():
            raise RecursionError("Recursive Improvement Loop Detected - Cascade depth limit reached")

        # Check regarding recursive improvement loops functionally
        recursive_improvements = len(list(
            filter(lambda e: e.get("failure_type") == "recursive_improvement", self.failure_history)
        ))
        if recursive_improvements >= 2:
            raise RecursionError("Recursive Improvement Loop Detected - Multiple recursive improvement failures")

        return CascadeContext(
            task_id=task_id,
            cascade_depth=self.cascade_depth + 1,
            depth_limit=self.depth_limit,
            tenant_id=self.tenant_id,
            security_scope=self.security_scope.copy(),
            failure_history=self.failure_history.copy()
        )

    def log_failure(self, stage: str, error: str, failure_type: str = "unknown") -> None:
        """Log a failure in the cascade context."""
        entry = {
            "stage": stage,
            "error": error,
            "failure_type": failure_type,
            "timestamp": time.time()
        }

        # Check regarding repeating errors functionally (circuit breaker)
        recent_matches = list(filter(
            lambda e: e.get("error") == error and e.get("stage") == stage,
            self.failure_history[-2:]
        ))
        if len(recent_matches) >= 2:
            # Replace the third occurrence with a circuit breaker
            entry = {
                "stage": "circuit_breaker_repeating",
                "error": f"Exact Repeating Error: {error} (Circuit Breaker Triggered)",
                "failure_type": "circuit_breaker",
                "timestamp": time.time()
            }

        self.failure_history.append(entry)

    def is_bursting(self) -> bool:
        """Check if recursion depth limit reached."""
        return self.cascade_depth >= self.depth_limit


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
        """Render the prompt template with context variables."""
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
        """Add a message to the history."""
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]


@dataclass(slots=True)
class SpeculativeProposal:
    """
    Draft proposal from a lower-tier agent to a higher-tier agent (Phase 56).
    Used in speculative swarm mode to accelerate decision making.
    """

    request_id: str
    draft_content: str
    confidence_score: float
    proposer_id: str
    metadata: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class VerificationOutcome:
    """
    Outcome of a speculative proposal verification (Phase 56).
    Determines if the draft was accepted, rejected, or partially modified.
    """

    proposal_id: str
    accepted: bool
    final_content: str
    accepted_length: int
    correction_applied: bool
    verifier_id: str
    latency_delta: float = 0.0


@dataclass(slots=True)
class AsyncSpeculativeToken:
    """
    A single token yielded by the speculative async pipeline (Phase 60).
    Includes a flag indicating if it's a 'draft' or 'verified' token.
    """

    token: str
    is_draft: bool
    sequence_index: int
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class PipelineCorrection:
    """
    signal to roll back and correct the output stream (Phase 60).
    """

    rollback_to_index: int
    correct_tokens: list[str]
    reason: str = "speculative_mismatch"


@dataclass(slots=True)
class ExpertProfile:
    """
    Metadata about an agent's expertise for MoE routing (Phase 61).
    """

    agent_id: str
    domains: list[str] = field(default_factory=_empty_list_str)
    performance_score: float = 1.0  # 0.0 to 1.0
    specialization_vector: list[float] = field(default_factory=_empty_list_str)  # Embedding
    model_family: str = "unknown"
    max_tokens: int = 4096
    is_replica: bool = False
    parent_id: str | None = None
    acceleration_type: str = "standard"  # standard, fp8_bitnet, h100_tensor, etc. (Phase 74)


@dataclass(slots=True)
class MoERoutingDecision:
    """
    The result of routing a task through the MoE Gatekeeper (Phase 61).
    """

    task_id: str
    selected_experts: list[str]  # Top-K agent IDs
    routing_weights: list[float]
    metadata: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class SwarmAuditTrail:
    """
    Detailed audit log for swarm decision making (Phase 69).
    Tracks routing, fusion, and expert selection reasoning.
    """

    request_id: str
    step: str  # "routing", "execution", "fusion"
    decision_summary: str
    raw_data: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0


@dataclass(slots=True)
class ExpertEvaluation:
    """
    Feedback evaluation for an expert's performance on a specific task (Phase 68).
    Used to drive Expert Specialization Evolution.
    """

    expert_id: str
    task_id: str
    is_correct: bool
    quality_score: float  # 0.0 to 1.0
    latency: float = 0.0
    feedback_notes: str = ""
    timestamp: float = field(default_factory=time.time)


class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        self.templates: dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        """Register a new template."""
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        """Render a registered template."""
        template = self.templates[template_name]
        return template.render(**kwargs)


class ResponsePostProcessor:
    """Manages post-processing hooks for agent responses."""

    def __init__(self) -> None:
        self.hooks: list[tuple[Callable[[str], str], int]] = []

    def register(self, hook: Callable[[str], str], priority: int = 0) -> None:
        """Register a post-processing hook."""
        self.hooks.append((hook, priority))

    def process(self, text: str) -> str:
        """Apply all registered hooks to the text."""
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

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
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

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        """Add an item to the batch."""
        if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        """Return the number of items in the batch."""
        return len(self.items)

    def execute(self, processor: Callable[[list[Any]], list[Any]]) -> list[Any]:
        """Execute the batch using the provided processor."""
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
        """Calculate total number of tokens used."""
        return sum(self.token_counts)

    @property
    def available_tokens(self) -> int:
        """Calculate remaining token budget."""
        return max(0, self.max_tokens - self.used_tokens)

    def add(self, message: str, token_count: int) -> None:
        """Add a message and its token count, enforcing max_tokens."""
        self.messages.append(message)
        self.token_counts.append(token_count)
        while self.used_tokens > self.max_tokens and self.messages:
            self.messages.pop(0)
            self.token_counts.pop(0)

    def clear(self) -> None:
        """Clear all messages from the window."""
        self.messages.clear()
        self.token_counts.clear()


@dataclass(slots=True)
class MultimodalBuilder:
    """Builds multimodal input sets."""

    inputs: list[MultimodalInput] = field(default_factory=list)

    def add(self, content: str, input_type: InputType) -> None:
        """Add a generic multimodal input."""
        self.inputs.append(MultimodalInput(content=content, input_type=input_type))

    def add_text(self, content: str) -> None:
        """Add text input."""
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.TEXT))

    def add_image(self, content: str) -> None:
        """Add image input."""
        self.inputs.append(MultimodalInput(content=content, input_type=InputType.IMAGE))

    def build(self) -> list[MultimodalInput]:
        """Return the list of built inputs."""
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
        """Initialize span context."""
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on the span."""
        self._span.attributes[key] = value

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """Add an event to the span."""
        self._span.events.append(
            {
                "name": name,
                "timestamp": time.time(),
                "attributes": attributes or {},
            }
        )
