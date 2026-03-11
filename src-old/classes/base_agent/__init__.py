#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/__init__.description.md

# __init__

**File**: `src\\classes\base_agent\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 70 imports  
**Lines**: 175  
**Complexity**: 0 (simple)

## Overview

BaseAgent module: Core classes and utilities for AI-powered agents.

## Dependencies

**Imports** (70):
- `agent.BaseAgent`
- `agent.DEFAULT_PROMPT_TEMPLATES`
- `managers.ABTest`
- `managers.AgentComposer`
- `managers.AuthManager`
- `managers.AuthenticationManager`
- `managers.BatchRequest`
- `managers.ConversationHistory`
- `managers.EventManager`
- `managers.FilePriorityManager`
- `managers.HealthChecker`
- `managers.ModelSelector`
- `managers.MultimodalProcessor`
- `managers.PluginManager`
- `managers.ProfileManager`
- ... and 55 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/__init__.improvements.md

# Improvements for __init__

**File**: `src\\classes\base_agent\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 175 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""BaseAgent module: Core classes and utilities for AI-powered agents."""

# ========== Models (Data Structures) ==========
# ========== Agent Core ==========
from .agent import DEFAULT_PROMPT_TEMPLATES, BaseAgent

# ========== Managers (Business Logic) ==========
from .managers import (
    # A/B Testing
    ABTest,
    # Agent Composition
    AgentComposer,
    # Authentication
    AuthenticationManager,
    AuthManager,
    # Batch Processing
    BatchRequest,
    ConversationHistory,
    # Event Management
    EventManager,
    # File Priority
    FilePriorityManager,
    # Health Checking
    HealthChecker,
    # Model Selection
    ModelSelector,
    # Multimodal Processing
    MultimodalProcessor,
    # Plugin Management
    PluginManager,
    # Configuration Profiles
    ProfileManager,
    # Prompt Management
    PromptTemplateManager,
    PromptVersion,
    PromptVersionManager,
    # Quality Scoring
    QualityScorer,
    RequestBatcher,
    # Response Caching
    ResponseCache,
    ResponsePostProcessor,
    # Serialization
    SerializationManager,
    # State Persistence
    StatePersistence,
)
from .models import (
    # Dataclasses
    AgentConfig,
    # Enums
    AgentEvent,
    AgentParallel,
    AgentPipeline,
    AgentRouter,
    AgentState,
    AgentType,
    AuthConfig,
    AuthMethod,
    BatchResult,
    CacheEntry,
    ComposedAgent,
    ConfigProfile,
    ContextWindow,
    ConversationMessage,
    EventHook,
    EventType,
    FilePriority,
    FilePriorityConfig,
    HealthCheckResult,
    InputType,
    MessageRole,
    ModelConfig,
    MultimodalBuilder,
    MultimodalInput,
    PromptTemplate,
    ResponseQuality,
    SerializationConfig,
    SerializationFormat,
    TokenBudget,
    _empty_agent_event_handlers,
    _empty_dict_str_any,
    _empty_dict_str_callable_any_any,
    _empty_dict_str_configprofile,
    _empty_dict_str_filepriority,
    _empty_dict_str_health_checks,
    _empty_dict_str_int,
    _empty_dict_str_modelconfig,
    _empty_dict_str_quality_criteria,
    _empty_dict_str_str,
    _empty_list_float,
    _empty_list_int,
    # Helper functions
    _empty_list_str,
    _empty_routes_list,
)
from .utilities import create_main_function, setup_logging

__all__ = [
    # Models/Enums
    "AgentEvent",
    "AgentState",
    "AgentType",
    "AuthMethod",
    "EventType",
    "FilePriority",
    "InputType",
    "MessageRole",
    "ResponseQuality",
    "SerializationFormat",
    "AgentConfig",
    "AgentParallel",
    "AgentPipeline",
    "AgentRouter",
    "AuthConfig",
    "BatchResult",
    "CacheEntry",
    "ComposedAgent",
    "ConfigProfile",
    "ContextWindow",
    "ConversationMessage",
    "EventHook",
    "FilePriorityConfig",
    "HealthCheckResult",
    "ModelConfig",
    "MultimodalBuilder",
    "MultimodalInput",
    "PromptTemplate",
    "SerializationConfig",
    "TokenBudget",
    # Managers
    "PromptTemplateManager",
    "PromptVersion",
    "PromptVersionManager",
    "ConversationHistory",
    "ResponsePostProcessor",
    "BatchRequest",
    "RequestBatcher",
    "AuthenticationManager",
    "AuthManager",
    "MultimodalProcessor",
    "AgentComposer",
    "SerializationManager",
    "FilePriorityManager",
    "ResponseCache",
    "StatePersistence",
    "ModelSelector",
    "QualityScorer",
    "ABTest",
    "EventManager",
    "PluginManager",
    "HealthChecker",
    "ProfileManager",
    # Core Agent
    "BaseAgent",
    "DEFAULT_PROMPT_TEMPLATES",
    "create_main_function",
    "setup_logging",
]

__version__ = "1.0.0"
__author__ = "PyAgent Contributors"
