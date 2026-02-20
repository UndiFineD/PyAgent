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


try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any, Dict, List
except ImportError:
    from typing import Any, Dict, List



@dataclass
class AgentTemplate:
    """A minimal agent template dataclass used by tests and code generation."""

    name: str
    description: str = ""
    agents: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    file_patterns: List[str] = field(default_factory=lambda: ["*.py"])
