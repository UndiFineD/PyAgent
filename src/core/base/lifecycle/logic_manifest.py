#!/usr/bin/env python3
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


"""Module: logic_manifest
Defines the cognitive structure and capability set for a Universal Agent.
"""


from __future__ import annotations

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any
except ImportError:
    from typing import Any



@dataclass
class LogicManifest:
    """
    The 'Logic Shard' that defines how an agent thinks and what it can do.
    This replaces hard-coded specialist logic.
    """
    version: str = "1.0.0"
    role: str = "generalist"
    description: str = "A universal autonomous agent"
    # Required skill cores to load
    required_skills: list[str] = field(default_factory=lambda: ["identity", "environment", "security"])
    # Cognitive configuration
    reasoning_mode: str = "cot"  # Chain of Thought
    memory_strategy: str = "autovault"
    # Permissions and Boundaries
    permissions: dict[str, Any] = field(default_factory=lambda: {
        "fs_read": True,
        "fs_write": False,
        "network": True,
        "execution": False
    })
    # Toolsets available
    tools: list[str] = field(default_factory=list)
    # Pillar 4: Industrial Factory (Branching Workflows)
    flow_nodes: list[dict[str, Any]] = field(default_factory=list)
    connectors: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LogicManifest:
        """Hydrate a manifest from a dictionary."""
# Ensure only known fields are passed
        valid_fields = cls.__dataclass_fields__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
