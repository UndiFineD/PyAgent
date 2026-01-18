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
Internal managers for prompt, conversation, auth, and batch processing.
"""

from __future__ import annotations
from src.core.base.version import VERSION as VERSION
from .PromptManagers import PromptTemplateManager as PromptTemplateManager, PromptVersion as PromptVersion, PromptVersionManager as PromptVersionManager
from .ConversationManagers import ConversationHistory as ConversationHistory
from .AuthManagers import AuthenticationManager as AuthenticationManager, AuthManager as AuthManager
from .BatchManagers import BatchRequest as BatchRequest, RequestBatcher as RequestBatcher
from .ProcessorManagers import ResponsePostProcessor as ResponsePostProcessor, MultimodalProcessor as MultimodalProcessor, SerializationManager as SerializationManager
from .OrchestrationManagers import AgentComposer as AgentComposer, ModelSelector as ModelSelector, QualityScorer as QualityScorer, ABTest as ABTest
from .PluginManager import PluginManager as PluginManager, PluginMetadata as PluginMetadata
from .SystemManagers import (
    FilePriorityManager as FilePriorityManager,
    ResponseCache as ResponseCache,
    StatePersistence as StatePersistence, 
    EventManager as EventManager,
    HealthChecker as HealthChecker,
    ProfileManager as ProfileManager
)
from .ResourceQuotaManager import ResourceQuotaManager as ResourceQuotaManager, QuotaConfig as QuotaConfig

__version__ = VERSION
