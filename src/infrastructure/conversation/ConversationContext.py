# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Conversation Context Management.
Delegates to modularized sub-packages in src/infrastructure/conversation/context/.
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
    ToolOrchestrator,
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
    "ToolOrchestrator",
]


