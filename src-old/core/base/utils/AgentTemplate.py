#!/usr/bin/env python3
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


from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentTemplate:
    """Lightweight container for agent template metadata.

    This class is intentionally minimal; more complex behavior can be
    added as needed by other components.  ``TemplateManager`` only uses
    the ``name`` attribute and expects the constructor to accept the
    keyword arguments demonstrated below.
    """

    name: str
    description: Optional[str] = None
    agents: List[str] = field(default_factory=list)
    file_patterns: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # ensure the name attribute is always a string
        self.name = str(self.name)
