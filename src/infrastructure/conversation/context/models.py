# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Conversation context models and enums.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ContextState(Enum):
    """Conversation context state."""
    ACTIVE = "active"
    WAITING_INPUT = "waiting_input"
    WAITING_TOOL = "waiting_tool"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    EXPIRED = "expired"


class TurnType(Enum):
    """Conversation turn type."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    REASONING = "reasoning"


class ToolExecutionPolicy(Enum):
    """Tool execution policy."""
    SEQUENTIAL = "sequential"  # Execute tools one at a time
    PARALLEL = "parallel"  # Execute tools in parallel
    BATCH = "batch"  # Batch similar tools
    LAZY = "lazy"  # Defer execution until needed


@dataclass
class TokenMetrics:
    """Token usage metrics."""
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    tool_tokens: int = 0
    reasoning_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def effective_input_tokens(self) -> int:
        """Input tokens minus cached."""
        return self.input_tokens - self.cached_tokens

    def add(self, other: "TokenMetrics") -> "TokenMetrics":
        """Add metrics."""
        return TokenMetrics(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_tokens=self.cached_tokens + other.cached_tokens,
            tool_tokens=self.tool_tokens + other.tool_tokens,
            reasoning_tokens=self.reasoning_tokens + other.reasoning_tokens,
        )

    def to_dict(self) -> Dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cached_tokens": self.cached_tokens,
            "tool_tokens": self.tool_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass
class ConversationTurn:
    """Single conversation turn."""
    id: str
    type: TurnType
    content: Any
    timestamp: float = field(default_factory=time.time)
    tokens: Optional[TokenMetrics] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    child_ids: List[str] = field(default_factory=list)

    def to_message(self) -> Dict[str, Any]:
        """Convert to message format."""
        role_map = {
            TurnType.SYSTEM: "system",
            TurnType.USER: "user",
            TurnType.ASSISTANT: "assistant",
            TurnType.TOOL_CALL: "assistant",
            TurnType.TOOL_RESULT: "tool",
            TurnType.REASONING: "assistant",
        }
        msg = {
            "role": role_map.get(self.type, "user"),
            "content": self.content if isinstance(self.content, str) else "",
        }
        if self.type == TurnType.TOOL_CALL and isinstance(self.content, list):
            msg["content"] = None
            msg["tool_calls"] = self.content
        if self.type == TurnType.TOOL_RESULT:
            msg["tool_call_id"] = self.metadata.get("tool_call_id", "")
        return msg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "tokens": self.tokens.to_dict() if self.tokens else None,
            "metadata": self.metadata,
        }


@dataclass
class ToolExecution:
    """Tool execution record."""
    call_id: str
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    status: str = "pending"

    @property
    def duration_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

    @property
    def is_complete(self) -> bool:
        return self.status in ("completed", "failed")


@dataclass
class ContextConfig:
    """Context configuration."""
    max_turns: int = 100
    max_tokens: int = 128000
    max_tool_calls_per_turn: int = 10
    max_parallel_tools: int = 5
    tool_timeout_seconds: float = 30.0
    tool_policy: ToolExecutionPolicy = ToolExecutionPolicy.SEQUENTIAL
    enable_reasoning: bool = True
    enable_caching: bool = True
    auto_summarize: bool = False
    summarize_threshold: int = 50

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_turns": self.max_turns,
            "max_tokens": self.max_tokens,
            "tool_policy": self.tool_policy.value,
            "enable_reasoning": self.enable_reasoning,
        }


@dataclass
class ContextSnapshot:
    """Snapshot of context state."""
    context_id: str
    timestamp: float
    state: ContextState
    turn_count: int
    total_tokens: TokenMetrics
    turns: List[ConversationTurn]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "timestamp": self.timestamp,
            "state": self.state.value,
            "turn_count": self.turn_count,
            "total_tokens": self.total_tokens.to_dict(),
            "turns": [t.to_dict() for t in self.turns],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextSnapshot":
        """Restore from dictionary."""
        turns = []
        for turn_data in data.get("turns", []):
            tokens = None
            if turn_data.get("tokens"):
                tokens = TokenMetrics(**turn_data["tokens"])
            turns.append(
                ConversationTurn(
                    id=turn_data["id"],
                    type=TurnType(turn_data["type"]),
                    content=turn_data["content"],
                    timestamp=turn_data.get("timestamp", 0),
                    tokens=tokens,
                    metadata=turn_data.get("metadata", {}),
                )
            )
        token_data = data.get("total_tokens", {})
        token_data = {k: v for k, v in token_data.items() if k != "total_tokens"}
        return cls(
            context_id=data["context_id"],
            timestamp=data["timestamp"],
            state=ContextState(data["state"]),
            turn_count=data["turn_count"],
            total_tokens=TokenMetrics(**token_data),
            turns=turns,
            metadata=data.get("metadata", {}),
        )
