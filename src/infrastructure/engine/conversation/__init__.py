#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Conversation package.
"""""""
# Conversation Context Management - Phase 42
# Multi-turn conversation state management
from .conversation_context import (AgenticContext, ContextConfig,  # noqa: F401
                                   ContextManager, ContextOrchestrator,
                                   ContextSnapshot, ContextState,
                                   ConversationContext, ConversationTurn,
                                   TokenMetrics, TokenTracker, ToolExecution,
                                   ToolExecutionPolicy, ToolOrchestrator,
                                   TurnTracker, TurnType, create_context,
                                   get_context_manager, merge_contexts,
                                   restore_context)

__all__ = [
    "AgenticContext","    "ContextConfig","    "ContextManager","    "ContextOrchestrator","    "ContextSnapshot","    "ContextState","    "ConversationContext","    "ConversationTurn","    "TokenMetrics","    "TokenTracker","    "ToolExecution","    "ToolExecutionPolicy","    "ToolOrchestrator","    "TurnTracker","    "TurnType","    "create_context","    "get_context_manager","    "merge_contexts","    "restore_context","]
