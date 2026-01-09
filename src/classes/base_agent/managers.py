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

from __future__ import annotations

"""Manager and utility classes for BaseAgent (Facade)."""

from .managers.PromptManagers import PromptTemplateManager, PromptVersion, PromptVersionManager
from .managers.ConversationManagers import ConversationHistory
from .managers.AuthManagers import AuthenticationManager, AuthManager
from .managers.BatchManagers import BatchRequest, RequestBatcher
from .managers.ProcessorManagers import ResponsePostProcessor, MultimodalProcessor, SerializationManager
from .managers.OrchestrationManagers import AgentComposer, ModelSelector, QualityScorer, ABTest
from .managers.SystemManagers import (
    FilePriorityManager, ResponseCache, StatePersistence, 
    EventManager, PluginManager, HealthChecker, ProfileManager
)
