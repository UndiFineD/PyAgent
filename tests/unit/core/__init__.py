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

# -*- coding: utf-8 -*-
"""Extracted test classes from test_base_agent.py."""

__all__ = [
    "TestAgentComposer",
    "TestAgentCompositionPatterns",
    "TestAgentConfig",
    "TestAgentConfigurationProfiles",
    "TestAgentEventHooks",
    "TestAgentHealthDiagnostics",
    "TestAgentPluginLoading",
    "TestAgentState",
    "TestAgentStatePersistence",
    "TestAuthenticationManager",
    "TestCacheManagement",
    "TestContentBasedResponseCaching",
    "TestContextWindow",
    "TestContextWindowManagement",
    "TestConversationHistory",
    "TestConversationHistoryManagement",
    "TestCustomAuthenticationMethods",
    "TestEventHooks",
    "TestEventType",
    "TestFilePriorityManager",
    "TestHealthCheckResult",
    "TestHealthChecks",
    "TestModelSelection",
    "TestModelSelectionPerAgentType",
    "TestMultimodalInputHandling",
    "TestMultimodalProcessor",
    "TestPluginSystem",
    "TestPostProcessors",
    "TestPromptTemplate",
    "TestPromptTemplates",
    "TestPromptTemplatingSystem",
    "TestPromptVersionManager",
    "TestPromptVersioningAndABTesting",
    "TestRequestBatcher",
    "TestRequestBatchingPerformance",
    "TestResponsePostProcessingHooks",
    "TestResponseQuality",
    "TestResponseQualityScoring",
    "TestResponseQualityScoring_v2",
    "TestSerializationManager",
    "TestSession8Dataclasses",
    "TestSession8Enums",
    "TestStatePersistence",
    "TestTokenBudget",
    "TestTokenBudgetManagement",
]

from .test_base_agent_unit import *  # noqa: F401, F403
from .test_base_agent_core_unit import *  # noqa: F401, F403
from .test_context_unit import *  # noqa: F401, F403
from .test_context_core_unit import *  # noqa: F401, F403
