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
Core primitives and base classes for PyAgent.
"""

from __future__ import annotations
from src.core.base.Version import VERSION as VERSION
from .BaseAgent import BaseAgent as BaseAgent
from .models import (
    AgentConfig as AgentConfig,
    AgentState as AgentState,
    ResponseQuality as ResponseQuality,
    PromptTemplate as PromptTemplate,
)
from .BaseInterfaces import (
    AgentInterface as AgentInterface,
    OrchestratorInterface as OrchestratorInterface,
)
from .AgentPluginBase import AgentPluginBase as AgentPluginBase
from .models.CoreEnums import HealthStatus as HealthStatus

__version__ = VERSION
