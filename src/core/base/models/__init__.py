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
from src.core.base.version import VERSION as VERSION

from .enums import (
    AgentState,
    ResponseQuality,
    EventType,
    AuthMethod,
    SerializationFormat,
    FilePriority,
    InputType,
    AgentType,
    MessageRole,
    AgentEvent,
    AgentExecutionState,
    AgentPriority,
    ConfigFormat,
    DiffOutputFormat,
    HealthStatus,
    LockType,
    RateLimitStrategy
)

from .base_models import (
    CacheEntry,
    AuthConfig,
    SerializationConfig,
    FilePriorityConfig,
    ExecutionCondition,
    ValidationRule,
    ModelConfig,
    ConfigProfile,
    DiffResult,
    EventHook,
    _empty_list_str,
    _empty_list_int,
    _empty_list_float,
    _empty_list_dict_str_any,
    _empty_dict_str_float,
    _empty_dict_str_any,
    _empty_dict_str_int,
    _empty_dict_str_str,
    _empty_dict_str_callable_any_any,
    _empty_dict_str_quality_criteria,
    _empty_dict_str_health_checks,
    _empty_dict_str_configprofile,
    _empty_agent_event_handlers,
    _empty_routes_list,
    _empty_dict_str_filepriority,
    _empty_dict_str_modelconfig
)

from .agent_models import (
    AgentConfig,
    ComposedAgent,
    AgentHealthCheck,
    AgentPluginConfig,
    ExecutionProfile,
    AgentPipeline,
    AgentParallel,
    AgentRouter
)

from .fleet_models import (
    HealthCheckResult,
    IncrementalState,
    ShutdownState,
    RateLimitConfig,
    TokenBudget
)

from .communication_models import (
    PromptTemplate,
    ConversationMessage,
    PromptVersion,
    BatchRequest,
    BatchResult,
    MultimodalInput,
    ContextWindow,
    CachedResult,
    TelemetrySpan,
    SpanContext,
    ConversationHistory,
    PromptTemplateManager,
    ResponsePostProcessor,
    MultimodalBuilder,
    CascadeContext
)

__version__ = VERSION

__all__ = [
    "AgentState", "ResponseQuality", "EventType", "AuthMethod", "SerializationFormat",
    "FilePriority", "InputType", "AgentType", "MessageRole", "AgentEvent",
    "AgentExecutionState", "AgentPriority", "ConfigFormat", "DiffOutputFormat",
    "HealthStatus", "LockType", "RateLimitStrategy", "CacheEntry", "AuthConfig",
    "SerializationConfig", "FilePriorityConfig", "ExecutionCondition", "ValidationRule",
    "ModelConfig", "ConfigProfile", "DiffResult", "EventHook", "AgentConfig", "ComposedAgent",
    "AgentHealthCheck", "AgentPluginConfig", "ExecutionProfile", "AgentPipeline",
    "AgentParallel", "AgentRouter", "HealthCheckResult", "IncrementalState",
    "ShutdownState", "RateLimitConfig", "TokenBudget", "PromptTemplate",
    "ConversationMessage", "PromptVersion", "BatchRequest", "BatchResult",
    "MultimodalInput", "ContextWindow", "CachedResult", "TelemetrySpan", "SpanContext",
    "ConversationHistory", "PromptTemplateManager", "ResponsePostProcessor",
    "MultimodalBuilder", "CascadeContext"
]
