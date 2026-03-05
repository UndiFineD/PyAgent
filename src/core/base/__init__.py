from __future__ import annotations

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

import sys

try:
    # Ensure imports using the uppercase module name succeed on case-insensitive
    # filesystems by aliasing the lowercase-loaded module into sys.modules.
    import src.core.base.version as _version_mod

    sys.modules.setdefault(
        "src.core.base.Version", sys.modules.get("src.core.base.version", _version_mod)
    )
except Exception:
    # Best-effort shim; if version can't be imported yet, don't fail package import
    pass

from src.core.base.common.base_interfaces import AgentInterface, OrchestratorInterface
from src.core.base.common.models import (
    AgentConfig,
    AgentState,
    PromptTemplate,
    ResponseQuality,
)
from src.core.base.common.models.core_enums import HealthStatus
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.agent_plugin_base import AgentPluginBase

__version__ = VERSION
__all__ = [
    "VERSION",
    "BaseAgent",
    "AgentConfig",
    "AgentState",
    "ResponseQuality",
    "PromptTemplate",
    "AgentInterface",
    "OrchestratorInterface",
    "AgentPluginBase",
    "HealthStatus",
]
