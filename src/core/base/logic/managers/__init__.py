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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""
Internal managers regarding prompt, conversation, auth, and batch processing.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .auth_manager import AuthenticationManager, AuthManager  # noqa: F401
from .batch_managers import BatchRequest, RequestBatcher  # noqa: F401
from .conversation_managers import ConversationHistory  # noqa: F401
from .orchestration_managers import (ABTest, AgentComposer, ModelSelector,  # noqa: F401
                                     QualityScorer)
from .plugin_manager import PluginManager, PluginMetadata  # noqa: F401
from .processor_managers import (MultimodalProcessor, ResponsePostProcessor,  # noqa: F401
                                 SerializationManager)
from .prompt_managers import (PromptTemplateManager, PromptVersion,  # noqa: F401
                              PromptVersionManager)
from .resource_quota_manager import QuotaConfig, ResourceQuotaManager  # noqa: F401
from .system_managers import (EventManager, FilePriorityManager, HealthChecker,  # noqa: F401
                              ProfileManager, ResponseCache, StatePersistence)

__version__ = VERSION
__all__ = [
    "PromptTemplateManager",
    "PromptVersion",
    "PromptVersionManager",
    "ConversationHistory",
    "AuthenticationManager",
    "AuthManager",
    "BatchRequest",
    "RequestBatcher",
    "ResponsePostProcessor",
    "MultimodalProcessor",
    "SerializationManager",
    "AgentComposer",
    "ModelSelector",
    "QualityScorer",
    "ABTest",
    "PluginManager",
    "PluginMetadata",
    "FilePriorityManager",
    "ResponseCache",
    "StatePersistence",
    "EventManager",
    "HealthChecker",
    "ProfileManager",
    "ResourceQuotaManager",
    "QuotaConfig",
]
