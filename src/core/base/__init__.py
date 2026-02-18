# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Core primitives and base classes for PyAgent.
"""

from src.core.base.common.base_interfaces import AgentInterface, OrchestratorInterface
from src.core.base.common.models import AgentConfig, AgentState, PromptTemplate, ResponseQuality
from src.core.base.common.models.core_enums import HealthStatus
from src.core.base.lifecycle.version import VERSION
from .logic.agent_plugin_base import AgentPluginBase


__version__ = VERSION
__all__ = [
    "VERSION",
    "AgentConfig",
    "AgentState",
    "ResponseQuality",
    "PromptTemplate",
    "AgentInterface",
    "OrchestratorInterface",
    "AgentPluginBase",
    "HealthStatus",
]
