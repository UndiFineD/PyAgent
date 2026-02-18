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


"""Auto-extracted class from agent_changes.py"""

from dataclasses import dataclass, field

try:
    from src.core.base.lifecycle.version import VERSION
except ImportError:
    try:
        from core.base.lifecycle.version import VERSION
    except ImportError:
        VERSION = "unknown"

__version__ = VERSION


@dataclass
class EntryTemplate:
    """Template for changelog entries with TODO: Placeholders.

    Attributes:
        name: Template name.
        template_text: Template with TODO: Placeholders.
        TODO: Placeholders: List of TODO: Placeholder names.
        description: Description of the template.
    """
    name: str
    template_text: str
    todo_placeholders: list[str] = field(default_factory=lambda: [])
    description: str = ""
