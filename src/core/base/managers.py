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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Manager and utility classes for BaseAgent (Facade)."""

from src.core.base.managers.PromptManagers import PromptTemplateManager, PromptVersion, PromptVersionManager
from src.core.base.managers.ConversationManagers import ConversationHistory
from src.core.base.managers.AuthManagers import AuthenticationManager, AuthManager
from src.core.base.managers.BatchManagers import BatchRequest, RequestBatcher
from src.core.base.managers.SystemManagers import (
    ResponsePostProcessor,
    MultimodalProcessor,
    AgentComposer,
    SerializationManager,
    FilePriorityManager,
    ResponseCache,
    StatePersistence,
    EventManager,
    PluginManager,
    HealthChecker,
    ProfileManager
)
from src.core.base.managers.ProcessorManagers import ResponsePostProcessor, MultimodalProcessor, SerializationManager
from src.core.base.managers.OrchestrationManagers import AgentComposer, ModelSelector, QualityScorer, ABTest
