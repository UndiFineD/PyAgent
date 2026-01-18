# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Conversation context management.
Note: This is a legacy facade. The implementation has been moved to the
'src.infrastructure.conversation.context' sub-package.
"""

from .context import (
    ContextConfig,
    ContextState,
    ContextSnapshot,
    TokenMetrics,
    TurnType,
    ConversationTurn,
    ToolExecution,
    ConversationContext,
    AgenticContext,
    ContextManager,
    get_context_manager,
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
    "ConversationContext",
    "AgenticContext",
    "ContextManager",
    "get_context_manager",
    "TurnTracker",
    "ToolOrchestrator",
]
