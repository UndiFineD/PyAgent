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
ImprovementTemplate - Template for creating improvements

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Construct: tpl = ImprovementTemplate(id="id", name="Name", title_pattern="Fix {area}", description_template="Change {detail}")
- Instantiate: tpl.instantiate({"area": "API", "detail": "endpoint X to Y"}) -> {"title": "...", "description": "..."}
- Tests may pass description_pattern instead of description_template; constructor handles that.

WHAT IT DOES:
- Provides a lightweight dataclass-style template object for producing improvement dicts with formatted title and description.
- Normalizes id/name defaults, preserves category/priority/effort, and offers instantiate(variables) to format patterns.

WHAT IT SHOULD DO BETTER:
- Validate and sanitize formatting variables to avoid KeyError or injection; consider using safe formatting (e.g., format_map with defaultdict) or templating library.
- Add explicit type-checking and runtime validation for category/priority/effort and clearer error messages.
- Provide methods for partial rendering, localization, and richer metadata (examples, tags), and add unit tests for edge cases (missing variables, non-str values).

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .effort_estimate import EffortEstimate
from .improvement_category import ImprovementCategory
from .improvement_priority import ImprovementPriority

__version__ = VERSION


@dataclass(init=False)
class ImprovementTemplate:
    """Template for creating improvements.

    Compatibility notes:
    - Tests construct templates without `id`/`category`.
    - Tests sometimes pass `description_pattern` instead of `description_template`.
    - `instantiate()` returns a dict with `title` and `description`.
    """

    id: str
    name: str
    category: ImprovementCategory
    title_pattern: str
    description_template: str
    default_priority: ImprovementPriority
    default_effort: EffortEstimate

    def __init__(
        self,
        id: str = "",
        name: str = "",
        category: ImprovementCategory = ImprovementCategory.OTHER,
        title_pattern: str = "",
        description_template: str = "",
        description_pattern: str = "",
        default_priority: ImprovementPriority = ImprovementPriority.MEDIUM,
        default_effort: EffortEstimate = EffortEstimate.MEDIUM,
        **_: Any,
    ) -> None:
        if not description_template and description_pattern:
            description_template = description_pattern

        resolved_id = (id or name or "template").strip()
        resolved_name = (name or resolved_id).strip()

        self.id = resolved_id
        self.name = resolved_name
        self.category = category
        self.title_pattern = title_pattern
        self.description_template = description_template
        self.default_priority = default_priority
        self.default_effort = default_effort

    def instantiate(self, variables: dict[str, str]) -> dict[str, str]:
        """Instantiate the template with variables."""
        return {
            "title": self.title_pattern.format(**variables),
            "description": self.description_template.format(**variables),
        }
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .effort_estimate import EffortEstimate
from .improvement_category import ImprovementCategory
from .improvement_priority import ImprovementPriority

__version__ = VERSION


@dataclass(init=False)
class ImprovementTemplate:
    """Template for creating improvements.

    Compatibility notes:
    - Tests construct templates without `id`/`category`.
    - Tests sometimes pass `description_pattern` instead of `description_template`.
    - `instantiate()` returns a dict with `title` and `description`.
    """

    id: str
    name: str
    category: ImprovementCategory
    title_pattern: str
    description_template: str
    default_priority: ImprovementPriority
    default_effort: EffortEstimate

    def __init__(
        self,
        id: str = "",
        name: str = "",
        category: ImprovementCategory = ImprovementCategory.OTHER,
        title_pattern: str = "",
        description_template: str = "",
        description_pattern: str = "",
        default_priority: ImprovementPriority = ImprovementPriority.MEDIUM,
        default_effort: EffortEstimate = EffortEstimate.MEDIUM,
        **_: Any,
    ) -> None:
        if not description_template and description_pattern:
            description_template = description_pattern

        resolved_id = (id or name or "template").strip()
        resolved_name = (name or resolved_id).strip()

        self.id = resolved_id
        self.name = resolved_name
        self.category = category
        self.title_pattern = title_pattern
        self.description_template = description_template
        self.default_priority = default_priority
        self.default_effort = default_effort

    def instantiate(self, variables: dict[str, str]) -> dict[str, str]:
        """Instantiate the template with variables."""
        return {
            "title": self.title_pattern.format(**variables),
            "description": self.description_template.format(**variables),
        }
