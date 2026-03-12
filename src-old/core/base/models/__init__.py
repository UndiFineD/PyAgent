#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/models/__init__.description.md

# __init__

**File**: `src\\core\base\\models\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 73 imports  
**Lines**: 125  
**Complexity**: 0 (simple)

## Overview

Data models for PyAgent.
Unified entry point for re-exporting all sub-modules.

## Dependencies

**Imports** (73):
- `__future__.annotations`
- `agent_models.AgentConfig`
- `agent_models.AgentHealthCheck`
- `agent_models.AgentParallel`
- `agent_models.AgentPipeline`
- `agent_models.AgentPluginConfig`
- `agent_models.AgentRouter`
- `agent_models.ComposedAgent`
- `agent_models.ExecutionProfile`
- `base_models.AuthConfig`
- `base_models.CacheEntry`
- `base_models.ConfigProfile`
- `base_models.DiffResult`
- `base_models.EventHook`
- `base_models.ExecutionCondition`
- ... and 58 more

---
*Auto-generated documentation*
## Source: src-old/core/base/models/__init__.improvements.md

# Improvements for __init__

**File**: `src\\core\base\\models\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 125 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

from src.core.base.version import VERSION as VERSION

from .agent_models import (
    AgentConfig,
    AgentHealthCheck,
    AgentParallel,
    AgentPipeline,
    AgentPluginConfig,
    AgentRouter,
    ComposedAgent,
    ExecutionProfile,
)
from .base_models import (
    AuthConfig,
    CacheEntry,
    ConfigProfile,
    DiffResult,
    EventHook,
    ExecutionCondition,
    FilePriorityConfig,
    ModelConfig,
    SerializationConfig,
    ValidationRule,
    _empty_agent_event_handlers,
    _empty_dict_str_any,
    _empty_dict_str_callable_any_any,
    _empty_dict_str_configprofile,
    _empty_dict_str_filepriority,
    _empty_dict_str_float,
    _empty_dict_str_health_checks,
    _empty_dict_str_int,
    _empty_dict_str_modelconfig,
    _empty_dict_str_quality_criteria,
    _empty_dict_str_str,
    _empty_list_dict_str_any,
    _empty_list_float,
    _empty_list_int,
    _empty_list_str,
    _empty_routes_list,
)
from .communication_models import (
    BatchRequest,
    BatchResult,
    CachedResult,
    CascadeContext,
    ContextWindow,
    ConversationHistory,
    ConversationMessage,
    MultimodalBuilder,
    MultimodalInput,
    PromptTemplate,
    PromptTemplateManager,
    PromptVersion,
    ResponsePostProcessor,
    SpanContext,
    TelemetrySpan,
)
from .enums import (
    AgentEvent,
    AgentExecutionState,
    AgentPriority,
    AgentState,
    AgentType,
    AuthMethod,
    ConfigFormat,
    DiffOutputFormat,
    EventType,
    FilePriority,
    HealthStatus,
    InputType,
    LockType,
    MessageRole,
    RateLimitStrategy,
    ResponseQuality,
    SerializationFormat,
)
from .fleet_models import HealthCheckResult, IncrementalState, RateLimitConfig, ShutdownState, TokenBudget

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
