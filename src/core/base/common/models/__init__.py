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
Data models for PyAgent.
Unified entry point for re-exporting all sub-modules.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .agent_models import (AgentConfig, AgentHealthCheck, AgentParallel,  # noqa: F401
                           AgentPipeline, AgentPluginConfig, AgentRouter,
                           ComposedAgent, ExecutionProfile)
from .base_models import (AuthConfig, CacheEntry, ConfigProfile, DiffResult,  # noqa: F401
                          EventHook, ExecutionCondition, FilePriorityConfig,
                          ModelConfig, SerializationConfig, ValidationRule,
                          _empty_agent_event_handlers)
from .communication_models import (BatchRequest, BatchResult, CachedResult,  # noqa: F401
                                   CascadeContext, ContextWindow,
                                   ConversationHistory, ConversationMessage,
                                   MultimodalBuilder, MultimodalInput,
                                   PromptTemplate, PromptTemplateManager,
                                   PromptVersion, ResponsePostProcessor,
                                   SpanContext, TelemetrySpan)
from .core_enums import (AgentEvent, AgentExecutionState, AgentPriority,  # noqa: F401
                         AgentState, AgentType, AuthMethod, ConfigFormat,
                         DiffOutputFormat, EventType, FilePriority,
                         HealthStatus, InputType, LockType, MessageRole,
                         RateLimitStrategy, ResponseQuality,
                         SerializationFormat)
from .fleet_models import (HealthCheckResult, IncrementalState,  # noqa: F401
                           RateLimitConfig, ShutdownState, TokenBudget)

__version__ = VERSION

__all__ = [
    "AgentState",
    "ResponseQuality",
    "EventType",
    "AuthMethod",
    "SerializationFormat",
    "FilePriority",
    "InputType",
    "AgentType",
    "MessageRole",
    "AgentEvent",
    "AgentExecutionState",
    "AgentPriority",
    "ConfigFormat",
    "DiffOutputFormat",
    "HealthStatus",
    "LockType",
    "RateLimitStrategy",
    "CacheEntry",
    "AuthConfig",
    "SerializationConfig",
    "FilePriorityConfig",
    "ExecutionCondition",
    "ValidationRule",
    "ModelConfig",
    "ConfigProfile",
    "DiffResult",
    "EventHook",
    "AgentConfig",
    "ComposedAgent",
    "AgentHealthCheck",
    "AgentPluginConfig",
    "ExecutionProfile",
    "AgentPipeline",
    "AgentParallel",
    "AgentRouter",
    "HealthCheckResult",
    "IncrementalState",
    "ShutdownState",
    "RateLimitConfig",
    "TokenBudget",
    "PromptTemplate",
    "ConversationMessage",
    "PromptVersion",
    "BatchRequest",
    "BatchResult",
    "MultimodalInput",
    "ContextWindow",
    "CachedResult",
    "TelemetrySpan",
    "SpanContext",
    "ConversationHistory",
    "PromptTemplateManager",
    "ResponsePostProcessor",
    "MultimodalBuilder",
    "CascadeContext",
    "_empty_agent_event_handlers",
]
