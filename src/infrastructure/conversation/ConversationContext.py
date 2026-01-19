# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Conversation context management.
Facade for the modularized implementation in src/infrastructure/conversation/context/.
"""

from __future__ import annotations

from .context import (
    ContextConfig,
    ContextState,
    ContextSnapshot,
    TokenMetrics,
    TurnType,
    ConversationTurn,
    ToolExecution,
    ToolExecutionPolicy,
    ConversationContext,
    AgenticContext,
    ContextManager,
    get_context_manager,
    create_context,
    merge_contexts,
    restore_context,
    TurnTracker,
    TokenTracker,
    ToolOrchestrator,
    ContextOrchestrator,
)

__all__ = [
    "ContextConfig",
    "ContextState",
    "ContextSnapshot",
    "TokenMetrics",
    "TurnType",
    "ConversationTurn",
    "ToolExecution",
    "ToolExecutionPolicy",
    "ConversationContext",
    "AgenticContext",
    "ContextManager",
    "get_context_manager",
    "create_context",
    "merge_contexts",
    "restore_context",
    "TurnTracker",
    "TokenTracker",
    "ToolOrchestrator",
    "ContextOrchestrator",
]
