#!/usr/bin/env python3
# ruff: noqa: F401
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Data models for PyAgent.
Unified entry point for re-exporting all sub-modules via lazy loading.
"""
from typing import TYPE_CHECKING, Any
from src.core.lazy_loader import ModuleLazyLoader

if TYPE_CHECKING:
    from .agent_models import (AgentConfig, AgentHealthCheck, AgentParallel,  # noqa: F401
                               AgentPipeline, AgentPluginConfig, AgentRouter,  # noqa: F401
                               ComposedAgent, ExecutionProfile)  # noqa: F401
    from .base_models import (AuthConfig, CacheEntry, ConfigProfile,  # noqa: F401
                              DiffResult, EventHook, ExecutionCondition,  # noqa: F401
                              FilePriorityConfig, ModelConfig,  # noqa: F401
                              SerializationConfig, ValidationRule)  # noqa: F401
    from .communication_models import (BatchRequest, BatchResult, CachedResult,  # noqa: F401
                                       CascadeContext, ContextWindow,  # noqa: F401
                                       ConversationHistory,  # noqa: F401
                                       ConversationMessage, MultimodalBuilder,  # noqa: F401
                                       MultimodalInput, PromptTemplate,  # noqa: F401
                                       PromptTemplateManager, PromptVersion,  # noqa: F401
                                       ResponsePostProcessor, SpanContext,  # noqa: F401
                                       TelemetrySpan)  # noqa: F401
    from .core_enums import (AgentEvent, AgentExecutionState, AgentPriority,  # noqa: F401
                             AgentState, AgentType, AuthMethod, ConfigFormat,  # noqa: F401
                             DiffOutputFormat, EventType, FailureClassification,  # noqa: F401
                             FilePriority, HealthStatus, InputType, LockType,  # noqa: F401
                             MessageRole, RateLimitStrategy, ResponseQuality,  # noqa: F401
                             SerializationFormat)  # noqa: F401
    from .fleet_models import (HealthCheckResult, IncrementalState,  # noqa: F401
                               RateLimitConfig, ShutdownState, TokenBudget)  # noqa: F401

_LAZY_REGISTRY = {
    # .core_enums
    "AgentEvent": ("src.core.base.common.models.core_enums", "AgentEvent"),
    "AgentExecutionState": ("src.core.base.common.models.core_enums", "AgentExecutionState"),
    "AgentPriority": ("src.core.base.common.models.core_enums", "AgentPriority"),
    "AgentState": ("src.core.base.common.models.core_enums", "AgentState"),
    "AgentType": ("src.core.base.common.models.core_enums", "AgentType"),
    "AuthMethod": ("src.core.base.common.models.core_enums", "AuthMethod"),
    "ConfigFormat": ("src.core.base.common.models.core_enums", "ConfigFormat"),
    "DiffOutputFormat": ("src.core.base.common.models.core_enums", "DiffOutputFormat"),
    "EventType": ("src.core.base.common.models.core_enums", "EventType"),
    "FailureClassification": ("src.core.base.common.models.core_enums", "FailureClassification"),
    "FilePriority": ("src.core.base.common.models.core_enums", "FilePriority"),
    "HealthStatus": ("src.core.base.common.models.core_enums", "HealthStatus"),
    "InputType": ("src.core.base.common.models.core_enums", "InputType"),
    "LockType": ("src.core.base.common.models.core_enums", "LockType"),
    "MessageRole": ("src.core.base.common.models.core_enums", "MessageRole"),
    "RateLimitStrategy": ("src.core.base.common.models.core_enums", "RateLimitStrategy"),
    "ResponseQuality": ("src.core.base.common.models.core_enums", "ResponseQuality"),
    "SerializationFormat": ("src.core.base.common.models.core_enums", "SerializationFormat"),
    # .agent_models
    "AgentConfig": ("src.core.base.common.models.agent_models", "AgentConfig"),
    "AgentHealthCheck": ("src.core.base.common.models.agent_models", "AgentHealthCheck"),
    "AgentParallel": ("src.core.base.common.models.agent_models", "AgentParallel"),
    "AgentPipeline": ("src.core.base.common.models.agent_models", "AgentPipeline"),
    "AgentPluginConfig": ("src.core.base.common.models.agent_models", "AgentPluginConfig"),
    "AgentRouter": ("src.core.base.common.models.agent_models", "AgentRouter"),
    "ComposedAgent": ("src.core.base.common.models.agent_models", "ComposedAgent"),
    "ExecutionProfile": ("src.core.base.common.models.agent_models", "ExecutionProfile"),
    # .base_models
    "AuthConfig": ("src.core.base.common.models.base_models", "AuthConfig"),
    "CacheEntry": ("src.core.base.common.models.base_models", "CacheEntry"),
    "ConfigProfile": ("src.core.base.common.models.base_models", "ConfigProfile"),
    "DiffResult": ("src.core.base.common.models.base_models", "DiffResult"),
    "EventHook": ("src.core.base.common.models.base_models", "EventHook"),
    "ExecutionCondition": ("src.core.base.common.models.base_models", "ExecutionCondition"),
    "FilePriorityConfig": ("src.core.base.common.models.base_models", "FilePriorityConfig"),
    "ModelConfig": ("src.core.base.common.models.base_models", "ModelConfig"),
    "SerializationConfig": ("src.core.base.common.models.base_models", "SerializationConfig"),
    "ValidationRule": ("src.core.base.common.models.base_models", "ValidationRule"),
    # .communication_models
    "BatchRequest": ("src.core.base.common.models.communication_models", "BatchRequest"),
    "BatchResult": ("src.core.base.common.models.communication_models", "BatchResult"),
    "CachedResult": ("src.core.base.common.models.communication_models", "CachedResult"),
    "CascadeContext": ("src.core.base.common.models.communication_models", "CascadeContext"),
    "ContextWindow": ("src.core.base.common.models.communication_models", "ContextWindow"),
    "ConversationHistory": ("src.core.base.common.models.communication_models", "ConversationHistory"),
    "ConversationMessage": ("src.core.base.common.models.communication_models", "ConversationMessage"),
    "MultimodalBuilder": ("src.core.base.common.models.communication_models", "MultimodalBuilder"),
    "MultimodalInput": ("src.core.base.common.models.communication_models", "MultimodalInput"),
    "PromptTemplate": ("src.core.base.common.models.communication_models", "PromptTemplate"),
    "PromptTemplateManager": ("src.core.base.common.models.communication_models", "PromptTemplateManager"),
    "PromptVersion": ("src.core.base.common.models.communication_models", "PromptVersion"),
    "ResponsePostProcessor": ("src.core.base.common.models.communication_models", "ResponsePostProcessor"),
    "SpanContext": ("src.core.base.common.models.communication_models", "SpanContext"),
    "TelemetrySpan": ("src.core.base.common.models.communication_models", "TelemetrySpan"),
    # .fleet_models
    "HealthCheckResult": ("src.core.base.common.models.fleet_models", "HealthCheckResult"),
    "IncrementalState": ("src.core.base.common.models.fleet_models", "IncrementalState"),
    "RateLimitConfig": ("src.core.base.common.models.fleet_models", "RateLimitConfig"),
    "ShutdownState": ("src.core.base.common.models.fleet_models", "ShutdownState"),
    "TokenBudget": ("src.core.base.common.models.fleet_models", "TokenBudget"),
}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)


def __getattr__(name: str) -> Any:
    """Lazy load attributes."""
    return _loader.load(name)


def __dir__() -> list[str]:
    """Return available names."""
    return list(globals().keys()) + _loader.available_names()


__all__ = list(_LAZY_REGISTRY.keys())
