#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""BaseAgent module: Core classes and utilities for AI-powered agents."""

# ========== Models (Data Structures) ==========
from .models import (
    # Enums
    AgentEvent,
    AgentState,
    AgentType,
    AuthMethod,
    EventType,
    FilePriority,
    InputType,
    MessageRole,
    ResponseQuality,
    SerializationFormat,
    # Dataclasses
    AgentConfig,
    AgentParallel,
    AgentPipeline,
    AgentRouter,
    AuthConfig,
    BatchResult,
    CacheEntry,
    ComposedAgent,
    ConfigProfile,
    ContextWindow,
    ConversationMessage,
    EventHook,
    FilePriorityConfig,
    HealthCheckResult,
    ModelConfig,
    MultimodalBuilder,
    MultimodalInput,
    PromptTemplate,
    SerializationConfig,
    TokenBudget,
    # Helper functions
    _empty_list_str,
    _empty_list_int,
    _empty_list_float,
    _empty_dict_str_any,
    _empty_dict_str_int,
    _empty_dict_str_str,
    _empty_dict_str_callable_any_any,
    _empty_dict_str_quality_criteria,
    _empty_dict_str_health_checks,
    _empty_dict_str_configprofile,
    _empty_routes_list,
    _empty_dict_str_filepriority,
    _empty_dict_str_modelconfig,
    _empty_agent_event_handlers,
)

# ========== Managers (Business Logic) ==========
from .managers import (
    # Prompt Management
    PromptTemplateManager,
    PromptVersion,
    PromptVersionManager,
    ConversationHistory,
    ResponsePostProcessor,
    # Batch Processing
    BatchRequest,
    RequestBatcher,
    # Authentication
    AuthenticationManager,
    AuthManager,
    # Multimodal Processing
    MultimodalProcessor,
    # Agent Composition
    AgentComposer,
    # Serialization
    SerializationManager,
    # File Priority
    FilePriorityManager,
    # Response Caching
    ResponseCache,
    # State Persistence
    StatePersistence,
    # Model Selection
    ModelSelector,
    # Quality Scoring
    QualityScorer,
    # A/B Testing
    ABTest,
    # Event Management
    EventManager,
    # Plugin Management
    PluginManager,
    # Health Checking
    HealthChecker,
    # Configuration Profiles
    ProfileManager,
)

# ========== Agent Core ==========
from .agent import BaseAgent, DEFAULT_PROMPT_TEMPLATES
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
__author__ = "DebVisor Contributors"
