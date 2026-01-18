"""
Conversation Context Management - Phase 42

Multi-turn conversation state management for agentic workflows.
Inspired by vLLM's conversation context module.

Key Features:
- Multi-turn state tracking
- Tool call orchestration
- Token metrics per turn
- Error recovery
- Async session cleanup

Performance: Uses Rust-accelerated context hashing.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
import uuid
import weakref
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Deque,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "ContextState",
    "TurnType",
    "ToolExecutionPolicy",
    # Data Classes
    "TokenMetrics",
    "ConversationTurn",
    "ToolExecution",
    "ContextConfig",
    "ContextSnapshot",
    # Main Classes
    "ConversationContext",
    "AgenticContext",
    "ContextManager",
    "TurnTracker",
    "ToolOrchestrator",
    # Functions
    "create_context",
    "restore_context",
    "merge_contexts",
]


# ============================================================================
# Enums
# ============================================================================


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


# ============================================================================
# Data Classes
# ============================================================================


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

    # Links
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
    summarize_threshold: int = 50  # turns before summarization

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
        # Remove total_tokens key if present (not a field)
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


# ============================================================================
# Turn Tracker
# ============================================================================


class TurnTracker:
    """Track conversation turns and token usage."""

    def __init__(self, config: Optional[ContextConfig] = None):
        self.config = config or ContextConfig()
        self._turns: List[ConversationTurn] = []
        self._total_tokens = TokenMetrics()
        self._turn_index: Dict[str, ConversationTurn] = {}

    @property
    def turns(self) -> List[ConversationTurn]:
        return self._turns

    @property
    def turn_count(self) -> int:
        return len(self._turns)

    @property
    def total_tokens(self) -> TokenMetrics:
        return self._total_tokens

    def add_turn(
        self,
        turn_type: TurnType,
        content: Any,
        tokens: Optional[TokenMetrics] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        """Add a turn to the conversation."""
        turn_id = f"turn_{uuid.uuid4().hex[:12]}"

        turn = ConversationTurn(
            id=turn_id,
            type=turn_type,
            content=content,
            tokens=tokens,
            parent_id=parent_id,
            metadata=metadata or {},
        )

        self._turns.append(turn)
        self._turn_index[turn_id] = turn

        if tokens:
            self._total_tokens = self._total_tokens.add(tokens)

        # Link to parent
        if parent_id and parent_id in self._turn_index:
            self._turn_index[parent_id].child_ids.append(turn_id)

        return turn

    def get_turn(self, turn_id: str) -> Optional[ConversationTurn]:
        """Get turn by ID."""
        return self._turn_index.get(turn_id)

    def get_messages(
        self,
        include_system: bool = True,
        include_reasoning: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get turns as messages."""
        messages = []
        for turn in self._turns:
            if turn.type == TurnType.SYSTEM and not include_system:
                continue
            if turn.type == TurnType.REASONING and not include_reasoning:
                continue
            messages.append(turn.to_message())
        return messages

    def get_recent(self, n: int) -> List[ConversationTurn]:
        """Get n most recent turns."""
        return self._turns[-n:]

    def clear(self) -> None:
        """Clear all turns."""
        self._turns.clear()
        self._turn_index.clear()
        self._total_tokens = TokenMetrics()

    def truncate(self, max_turns: Optional[int] = None) -> int:
        """Truncate old turns."""
        limit = max_turns or self.config.max_turns
        if len(self._turns) <= limit:
            return 0

        removed = len(self._turns) - limit
        old_turns = self._turns[:removed]
        self._turns = self._turns[removed:]

        # Update index
        for turn in old_turns:
            self._turn_index.pop(turn.id, None)

        return removed


# ============================================================================
# Tool Orchestrator
# ============================================================================


class ToolOrchestrator:
    """Orchestrate tool execution within conversation."""

    def __init__(
        self,
        config: Optional[ContextConfig] = None,
        tool_handler: Optional[Callable] = None,
    ):
        self.config = config or ContextConfig()
        self.tool_handler = tool_handler
        self._pending: Dict[str, ToolExecution] = {}
        self._completed: List[ToolExecution] = []

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def has_pending(self) -> bool:
        return self.pending_count > 0

    def queue_tool_call(
        self,
        call_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> ToolExecution:
        """Queue a tool call for execution."""
        execution = ToolExecution(
            call_id=call_id,
            tool_name=tool_name,
            arguments=arguments,
        )
        self._pending[call_id] = execution
        return execution

    async def execute_pending(self) -> List[ToolExecution]:
        """Execute all pending tool calls."""
        if not self._pending:
            return []

        if self.config.tool_policy == ToolExecutionPolicy.PARALLEL:
            return await self._execute_parallel()
        else:
            return await self._execute_sequential()

    async def _execute_sequential(self) -> List[ToolExecution]:
        """Execute tools sequentially."""
        results = []
        for call_id, execution in list(self._pending.items()):
            await self._execute_one(execution)
            results.append(execution)
            self._completed.append(execution)
            del self._pending[call_id]
        return results

    async def _execute_parallel(self) -> List[ToolExecution]:
        """Execute tools in parallel."""
        max_parallel = self.config.max_parallel_tools

        pending_list = list(self._pending.values())
        results = []

        for i in range(0, len(pending_list), max_parallel):
            batch = pending_list[i : i + max_parallel]
            tasks = [self._execute_one(ex) for ex in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch)

        for ex in results:
            self._completed.append(ex)
            self._pending.pop(ex.call_id, None)

        return results

    async def _execute_one(self, execution: ToolExecution) -> None:
        """Execute a single tool."""
        execution.start_time = time.time()
        execution.status = "running"

        try:
            if self.tool_handler:
                result = await self._call_handler(execution)
                execution.result = result
                execution.status = "completed"
            else:
                execution.error = "No tool handler configured"
                execution.status = "failed"

        except asyncio.TimeoutError:
            execution.error = "Tool execution timed out"
            execution.status = "failed"

        except Exception as e:
            execution.error = str(e)
            execution.status = "failed"

        finally:
            execution.end_time = time.time()

    async def _call_handler(self, execution: ToolExecution) -> Any:
        """Call the tool handler."""
        if asyncio.iscoroutinefunction(self.tool_handler):
            return await asyncio.wait_for(
                self.tool_handler(execution.tool_name, execution.arguments),
                timeout=self.config.tool_timeout_seconds,
            )
        else:
            return self.tool_handler(execution.tool_name, execution.arguments)

    def get_results(self) -> List[ToolExecution]:
        """Get completed tool executions."""
        return list(self._completed)

    def clear_completed(self) -> None:
        """Clear completed executions."""
        self._completed.clear()


# ============================================================================
# Conversation Context (Base)
# ============================================================================


class ConversationContext(ABC):
    """
    Abstract base class for conversation context.
    
    Manages multi-turn conversation state, token tracking,
    and provides recovery mechanisms.
    """

    def __init__(
        self,
        context_id: Optional[str] = None,
        config: Optional[ContextConfig] = None,
    ):
        self.context_id = context_id or f"ctx_{uuid.uuid4().hex[:16]}"
        self.config = config or ContextConfig()
        self._state = ContextState.ACTIVE
        self._created_at = time.time()
        self._last_activity = time.time()
        self._turn_tracker = TurnTracker(config)
        self._metadata: Dict[str, Any] = {}

    @property
    def state(self) -> ContextState:
        return self._state

    @property
    def turns(self) -> List[ConversationTurn]:
        return self._turn_tracker.turns

    @property
    def turn_count(self) -> int:
        return self._turn_tracker.turn_count

    @property
    def total_tokens(self) -> TokenMetrics:
        return self._turn_tracker.total_tokens

    @property
    def is_active(self) -> bool:
        return self._state in (
            ContextState.ACTIVE,
            ContextState.WAITING_INPUT,
            ContextState.WAITING_TOOL,
            ContextState.PROCESSING,
        )

    def add_system(
        self,
        content: str,
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add system message."""
        self._update_activity()
        return self._turn_tracker.add_turn(TurnType.SYSTEM, content, tokens)

    def add_user(
        self,
        content: str,
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add user message."""
        self._update_activity()
        self._state = ContextState.PROCESSING
        return self._turn_tracker.add_turn(TurnType.USER, content, tokens)

    def add_assistant(
        self,
        content: str,
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add assistant message."""
        self._update_activity()
        self._state = ContextState.WAITING_INPUT
        return self._turn_tracker.add_turn(TurnType.ASSISTANT, content, tokens)

    def add_tool_call(
        self,
        tool_calls: List[Dict[str, Any]],
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add tool call."""
        self._update_activity()
        self._state = ContextState.WAITING_TOOL
        return self._turn_tracker.add_turn(TurnType.TOOL_CALL, tool_calls, tokens)

    def add_tool_result(
        self,
        tool_call_id: str,
        result: str,
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add tool result."""
        self._update_activity()
        return self._turn_tracker.add_turn(
            TurnType.TOOL_RESULT,
            result,
            tokens,
            metadata={"tool_call_id": tool_call_id},
        )

    def add_reasoning(
        self,
        content: str,
        tokens: Optional[TokenMetrics] = None,
    ) -> ConversationTurn:
        """Add reasoning (if enabled)."""
        if not self.config.enable_reasoning:
            return None

        self._update_activity()
        return self._turn_tracker.add_turn(TurnType.REASONING, content, tokens)

    def get_messages(
        self,
        include_system: bool = True,
        include_reasoning: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get conversation as messages."""
        return self._turn_tracker.get_messages(include_system, include_reasoning)

    def complete(self) -> None:
        """Mark context as completed."""
        self._state = ContextState.COMPLETED
        self._update_activity()

    def error(self, message: Optional[str] = None) -> None:
        """Mark context as errored."""
        self._state = ContextState.ERROR
        if message:
            self._metadata["error"] = message
        self._update_activity()

    def snapshot(self) -> ContextSnapshot:
        """Create snapshot of current state."""
        return ContextSnapshot(
            context_id=self.context_id,
            timestamp=time.time(),
            state=self._state,
            turn_count=self.turn_count,
            total_tokens=self.total_tokens,
            turns=list(self.turns),
            metadata=dict(self._metadata),
        )

    @classmethod
    def from_snapshot(cls, snapshot: ContextSnapshot) -> "ConversationContext":
        """Restore from snapshot."""
        ctx = cls(context_id=snapshot.context_id)
        ctx._state = snapshot.state
        ctx._metadata = snapshot.metadata

        for turn in snapshot.turns:
            ctx._turn_tracker._turns.append(turn)
            ctx._turn_tracker._turn_index[turn.id] = turn

        ctx._turn_tracker._total_tokens = snapshot.total_tokens
        return ctx

    def _update_activity(self) -> None:
        """Update last activity timestamp."""
        self._last_activity = time.time()

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources."""
        ...


# ============================================================================
# Agentic Context
# ============================================================================


class AgenticContext(ConversationContext):
    """
    Context for agentic workflows with tool orchestration.
    
    Extends base context with:
    - Tool execution management
    - Automatic tool call handling
    - State machine for agent loop
    """

    def __init__(
        self,
        context_id: Optional[str] = None,
        config: Optional[ContextConfig] = None,
        tool_handler: Optional[Callable] = None,
    ):
        super().__init__(context_id, config)
        self._tool_orchestrator = ToolOrchestrator(config, tool_handler)
        self._max_iterations = 10

    @property
    def tool_orchestrator(self) -> ToolOrchestrator:
        return self._tool_orchestrator

    @property
    def has_pending_tools(self) -> bool:
        return self._tool_orchestrator.has_pending

    def queue_tool_calls(
        self,
        tool_calls: List[Dict[str, Any]],
    ) -> List[ToolExecution]:
        """Queue tool calls from assistant response."""
        executions = []
        for tc in tool_calls:
            func = tc.get("function", {})
            execution = self._tool_orchestrator.queue_tool_call(
                call_id=tc.get("id", str(uuid.uuid4())),
                tool_name=func.get("name", ""),
                arguments=json.loads(func.get("arguments", "{}")),
            )
            executions.append(execution)
        return executions

    async def execute_tools(self) -> List[ToolExecution]:
        """Execute queued tool calls."""
        if not self.has_pending_tools:
            return []

        results = await self._tool_orchestrator.execute_pending()

        # Add results to conversation
        for execution in results:
            result_str = ""
            if execution.status == "completed":
                result_str = json.dumps(execution.result) if not isinstance(
                    execution.result, str
                ) else execution.result
            else:
                result_str = f"Error: {execution.error}"

            self.add_tool_result(
                execution.call_id,
                result_str,
                TokenMetrics(tool_tokens=len(result_str.split())),
            )

        return results

    async def run_agent_loop(
        self,
        generate_fn: Callable,
        initial_messages: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Run agentic loop until completion.
        
        Args:
            generate_fn: Async function to generate responses
            initial_messages: Starting messages
            
        Returns:
            Final assistant response
        """
        # Initialize with messages
        if initial_messages:
            for msg in initial_messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    self.add_system(content)
                elif role == "user":
                    self.add_user(content)
                elif role == "assistant":
                    self.add_assistant(content)

        iterations = 0
        final_response = ""

        while iterations < self._max_iterations and self.is_active:
            iterations += 1

            # Generate response
            messages = self.get_messages()
            response = await generate_fn(messages)

            # Check for tool calls
            tool_calls = response.get("tool_calls")
            if tool_calls:
                self.add_tool_call(tool_calls)
                self.queue_tool_calls(tool_calls)
                await self.execute_tools()
            else:
                # Final response
                final_response = response.get("content", "")
                self.add_assistant(final_response)
                self.complete()
                break

        if iterations >= self._max_iterations:
            self.error("Max iterations exceeded")

        return final_response

    async def cleanup(self) -> None:
        """Cleanup resources."""
        self._tool_orchestrator.clear_completed()
        self._turn_tracker.clear()
        self._state = ContextState.EXPIRED


# ============================================================================
# Context Manager
# ============================================================================


class ContextManager:
    """Manage multiple conversation contexts."""

    _instance: Optional["ContextManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._contexts = {}
            cls._instance._cleanup_task = None
        return cls._instance

    @property
    def contexts(self) -> Dict[str, ConversationContext]:
        return self._contexts

    def create(
        self,
        context_type: Type[ConversationContext] = ConversationContext,
        config: Optional[ContextConfig] = None,
        **kwargs,
    ) -> ConversationContext:
        """Create a new context."""
        if context_type == ConversationContext:
            # Use AgenticContext as default concrete implementation
            context_type = AgenticContext

        ctx = context_type(config=config, **kwargs)
        self._contexts[ctx.context_id] = ctx
        return ctx

    def get(self, context_id: str) -> Optional[ConversationContext]:
        """Get context by ID."""
        return self._contexts.get(context_id)

    async def cleanup(self, context_id: str) -> bool:
        """Cleanup and remove a context."""
        ctx = self._contexts.pop(context_id, None)
        if ctx:
            await ctx.cleanup()
            return True
        return False

    async def cleanup_expired(self, max_age_seconds: float = 3600) -> int:
        """Cleanup expired contexts."""
        now = time.time()
        expired = []

        for ctx_id, ctx in self._contexts.items():
            if now - ctx._last_activity > max_age_seconds:
                expired.append(ctx_id)

        for ctx_id in expired:
            await self.cleanup(ctx_id)

        return len(expired)

    def start_cleanup_task(self, interval_seconds: float = 300) -> None:
        """Start periodic cleanup task."""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(interval_seconds)
                try:
                    count = await self.cleanup_expired()
                    if count > 0:
                        logger.info(f"Cleaned up {count} expired contexts")
                except Exception as e:
                    logger.warning(f"Cleanup error: {e}")

        self._cleanup_task = asyncio.create_task(cleanup_loop())


# ============================================================================
# Convenience Functions
# ============================================================================


def create_context(
    config: Optional[ContextConfig] = None,
    tool_handler: Optional[Callable] = None,
) -> ConversationContext:
    """
    Create a new conversation context.
    
    Args:
        config: Context configuration
        tool_handler: Handler for tool calls
        
    Returns:
        New conversation context
    """
    return AgenticContext(config=config, tool_handler=tool_handler)


def restore_context(snapshot: ContextSnapshot) -> ConversationContext:
    """
    Restore context from snapshot.
    
    Args:
        snapshot: Context snapshot
        
    Returns:
        Restored context
    """
    return AgenticContext.from_snapshot(snapshot)


def merge_contexts(
    contexts: List[ConversationContext],
    config: Optional[ContextConfig] = None,
) -> ConversationContext:
    """
    Merge multiple contexts into one.
    
    Args:
        contexts: Contexts to merge
        config: Config for merged context
        
    Returns:
        Merged context
    """
    merged = AgenticContext(config=config)

    for ctx in contexts:
        for turn in ctx.turns:
            merged._turn_tracker._turns.append(turn)
            merged._turn_tracker._turn_index[turn.id] = turn

        merged._turn_tracker._total_tokens = merged._turn_tracker._total_tokens.add(
            ctx.total_tokens
        )

    return merged


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_context_hash(context: ConversationContext) -> Optional[str]:
    """Try Rust-accelerated context hashing."""
    try:
        from rust_core import hash_conversation_context_rust

        messages = [t.to_message() for t in context.turns]
        return hash_conversation_context_rust(messages)
    except ImportError:
        return None


def _try_rust_token_count(text: str) -> Optional[int]:
    """Try Rust-accelerated token counting."""
    try:
        from rust_core import fast_token_count_rust

        return fast_token_count_rust(text)
    except ImportError:
        return None
