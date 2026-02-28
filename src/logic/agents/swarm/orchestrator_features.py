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
OrchestratorFeatures: Mixin class for OrchestratorAgent features.
"""

from __future__ import annotations

from .orchestrator_diff_mixin import OrchestratorDiffMixin
from .orchestrator_execution_mixin import OrchestratorExecutionMixin
from .orchestrator_lifecycle_mixin import OrchestratorLifecycleMixin
from .orchestrator_plugin_mixin import OrchestratorPluginMixin
from .orchestrator_resource_mixin import OrchestratorResourceMixin


class OrchestratorFeatures(
    OrchestratorPluginMixin,
    OrchestratorResourceMixin,
    OrchestratorDiffMixin,
    OrchestratorLifecycleMixin,
    OrchestratorExecutionMixin,
):  # pylint: disable=too-many-ancestors
    """
    Mixin class that provides additional features to OrchestratorAgent.
    This helps keep the main OrchestratorAgent file small (<30KB).
    """
