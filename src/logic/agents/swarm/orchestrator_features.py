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
OrchestratorFeatures - Mixin aggregator for OrchestratorAgent features

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Import and use OrchestratorFeatures as a mixin base for OrchestratorAgent to compose plugin, resource, diffing, lifecycle, execution and work-pattern behavior without inflating the primary agent class; e.g., class OrchestratorAgent(OrchestratorFeatures, BaseAgent): ...

WHAT IT DOES:
Provides a single, small mixin container that aggregates related orchestrator feature mixins (plugin, resource, diff, lifecycle, execution, work-pattern) so the main OrchestratorAgent implementation stays compact and focused on orchestration concerns.

WHAT IT SHOULD DO BETTER:
- Document the initialization contract and expected attributes each mixin requires so composition is explicit and safe.
- Ensure deterministic initialization order and consider explicit __init__ chaining or an initialize_features() hook to avoid hidden coupling between mixins.
- Add type annotations and public API surface documentation for each mixed-in capability, plus unit tests that verify composed behavior and lifecycle interactions.
- Consider lazy-loading heavy resources (plugins, executors) and limiting the number of ancestor mixins to keep single-responsibility and easier testing.

FILE CONTENT SUMMARY:
OrchestratorFeatures: Mixin class for OrchestratorAgent features.
"""

from __future__ import annotations

from .orchestrator_diff_mixin import OrchestratorDiffMixin
from .orchestrator_execution_mixin import OrchestratorExecutionMixin
from .orchestrator_lifecycle_mixin import OrchestratorLifecycleMixin
from .orchestrator_plugin_mixin import OrchestratorPluginMixin
from .orchestrator_resource_mixin import OrchestratorResourceMixin
from .orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin


class OrchestratorFeatures(
    OrchestratorPluginMixin,
    OrchestratorResourceMixin,
    OrchestratorDiffMixin,
    OrchestratorLifecycleMixin,
    OrchestratorExecutionMixin,
    OrchestratorWorkPatternMixin,
):  # pylint: disable=too-many-ancestors
    """
    Mixin class that provides additional features to OrchestratorAgent.
    This helps keep the main OrchestratorAgent file small (<30KB).
    """
"""

from __future__ import annotations

from .orchestrator_diff_mixin import OrchestratorDiffMixin
from .orchestrator_execution_mixin import OrchestratorExecutionMixin
from .orchestrator_lifecycle_mixin import OrchestratorLifecycleMixin
from .orchestrator_plugin_mixin import OrchestratorPluginMixin
from .orchestrator_resource_mixin import OrchestratorResourceMixin
from .orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin


class OrchestratorFeatures(
    OrchestratorPluginMixin,
    OrchestratorResourceMixin,
    OrchestratorDiffMixin,
    OrchestratorLifecycleMixin,
    OrchestratorExecutionMixin,
    OrchestratorWorkPatternMixin,
):  # pylint: disable=too-many-ancestors
    """
    Mixin class that provides additional features to OrchestratorAgent.
    This helps keep the main OrchestratorAgent file small (<30KB).
    """
