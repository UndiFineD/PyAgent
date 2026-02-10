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

from typing import List, Optional, Dict, Any
from dataclasses import field
from pydantic import BaseModel


class AgentCard(BaseModel):
    """
    Standardized metadata for an agent in the fleet.
    Enables cross-agent discovery and orchestration.
    Harvested from .external/agentic_design_patterns pattern.
    """
    id: str
    name: str
    version: str = "1.0.0"
    description: str
    tier: str = "specialized"  # specialized, integrated, elite
    skills: List[str] = field(default_factory=list)
    input_modes: List[str] = field(default_factory=lambda: ["text"])
    output_modes: List[str] = field(default_factory=lambda: ["text"])
    config_schema: Dict[str, Any] = field(default_factory=dict)
    owner_team: Optional[str] = None
    last_updated: float = field(default_factory=lambda: 0.0)

    class Config:
        arbitrary_types_allowed = True
