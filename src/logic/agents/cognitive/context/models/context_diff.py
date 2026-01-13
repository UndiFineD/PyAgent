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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass, field
from typing import List

__version__ = VERSION

@dataclass
class ContextDiff:
    """Diff between context versions.

    Attributes:
        version_from: Source version.
        version_to: Target version.
        added_sections: List of added sections.
        removed_sections: List of removed sections.
        modified_sections: List of modified section names.
        change_summary: Brief summary of changes.
    """
    version_from: str
    version_to: str
    added_sections: List[str] = field(default_factory=lambda: [])
    removed_sections: List[str] = field(default_factory=lambda: [])
    modified_sections: List[str] = field(default_factory=lambda: [])
    change_summary: str = ""