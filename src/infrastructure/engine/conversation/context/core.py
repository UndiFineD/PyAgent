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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Core conversation context classes.
"""

from __future__ import annotations

import json
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from .models import (ContextConfig, ContextSnapshot, ContextState,
                     ConversationTurn, TokenMetrics, ToolExecution, TurnType)
from .orchestrator import ToolOrchestrator
from .tracker import TurnTracker


class ConversationContext(ABC):
    """
    Abstract base class for conversation context.
    """

    def __init__(
        self,
        context_id: Optional[str] = None,
        config: Optional[ContextConfig] = None,
    ) -> None:
        self.context_id = context_id or f"ctx_{uuid.uuid4().hex[:16]}"
        self.config = config or ContextConfig()
        self._state = ContextState.ACTIVE
        self._created_at = time.time()
        self._last_activity = time.time()
        self._turn_tracker = TurnTracker(config)
        self._metadata: dict[str, Any] = {}

    @property
    def state(self) -> ContextState:
        """Get the current state of the context."""
        return self._state

    @property
    def last_activity(self) -> float:
        """Get the timestamp of the last activity."""
        return self._last_activity

    @property
    def turns(self) -> list[ConversationTurn]:
        """Get all turns in this conversation."""
        return self._turn_tracker.turns

    @property
    def turn_count(self) -> int:
        """Get the total number of turns."""
        return self._turn_tracker.turn_count

    @property
    def total_tokens(self) -> TokenMetrics:
        """Get aggregate token metrics for all turns."""
        return self._turn_tracker.total_tokens

    @property
    def is_active(self) -> bool:
        """Check if the context is currently active."""
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
        tool_calls: list[dict[str, Any]],
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
    ) -> list[dict[str, Any]]:
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
            ctx._turn_tracker.append_turn(turn)

        ctx._turn_tracker._total_tokens = snapshot.total_tokens  # pylint: disable=protected-access
        return ctx

    def import_turns(self, turns: list[ConversationTurn], deduplicate: bool = True) -> None:
        """Import turns from another context."""
        seen_ids = {t.id for t in self.turns} if deduplicate else set()
        for turn in turns:
            if deduplicate and turn.id in seen_ids:
                continue
            self._turn_tracker.append_turn(turn)
        self._update_activity()

    def _update_activity(self) -> None:
        """Update last activity timestamp."""
        self._last_activity = time.time()

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources."""


class AgenticContext(ConversationContext):
    """
    Context for agentic workflows with tool orchestration.
    """

    def __init__(
        self,
        context_id: Optional[str] = None,
        config: Optional[ContextConfig] = None,
        tool_handler: Optional[Callable] = None,
    ) -> None:
        super().__init__(context_id, config)
        self._tool_orchestrator = ToolOrchestrator(config, tool_handler)
        self._max_iterations = 10

    @property
    def tool_orchestrator(self) -> ToolOrchestrator:
        """Return the tool orchestrator instance."""
        return self._tool_orchestrator

    @property
    def has_pending_tools(self) -> bool:
        """Check if there are pending tool executions."""
        return self._tool_orchestrator.has_pending

    def queue_tool_calls(
        self,
        tool_calls: list[dict[str, Any]],
    ) -> list[ToolExecution]:
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

    async def execute_tools(self) -> list[ToolExecution]:
        """Execute queued tool calls."""
        if not self.has_pending_tools:
            return []

        results = await self._tool_orchestrator.execute_pending()

        # Add results to conversation
        for execution in results:
            result_str = ""
            if execution.status == "completed":
                if not isinstance(execution.result, str):
                    result_str = json.dumps(execution.result)
                else:
                    result_str = execution.result
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
        initial_messages: Optional[list[dict[str, Any]]] = None,
    ) -> str:
        """Run agentic loop until completion."""
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
            messages = self.get_messages()
            response = await generate_fn(messages)

            tool_calls = response.get("tool_calls")
            if tool_calls:
                self.add_tool_call(tool_calls)
                self.queue_tool_calls(tool_calls)
                await self.execute_tools()
            else:
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
