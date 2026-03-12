#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/mixins/ChangesTemplateMixin.description.md

# ChangesTemplateMixin

**File**: `src\\logic\agents\\swarm\\mixins\\ChangesTemplateMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Template management logic for ChangesAgent.

## Classes (1)

### `ChangesTemplateMixin`

Mixin for managing changelog templates.

**Methods** (3):
- `set_template(self, template_name)`
- `create_custom_template(self, name, project_type, sections, header_format, include_links, include_contributors)`
- `get_template_sections(self)`

## Dependencies

**Imports** (4):
- `ChangelogTemplate.ChangelogTemplate`
- `__future__.annotations`
- `logging`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/mixins/ChangesTemplateMixin.improvements.md

# Improvements for ChangesTemplateMixin

**File**: `src\\logic\agents\\swarm\\mixins\\ChangesTemplateMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ChangesTemplateMixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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
Template management logic for ChangesAgent.
"""

import logging
from typing import List

from ..ChangelogTemplate import ChangelogTemplate


class ChangesTemplateMixin:
    """Mixin for managing changelog templates."""

    # Default templates for different project types
    DEFAULT_TEMPLATES: dict[str, ChangelogTemplate] = {
        "python": ChangelogTemplate(
            name="Python",
            project_type="python",
            sections=["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"],
            include_contributors=True,
        ),
        "javascript": ChangelogTemplate(
            name="JavaScript",
            project_type="javascript",
            sections=["Features", "Bug Fixes", "Breaking Changes", "Documentation"],
        ),
        "generic": ChangelogTemplate(
            name="Generic",
            project_type="generic",
            sections=["Added", "Changed", "Fixed", "Removed"],
        ),
    }

    def set_template(self, template_name: str) -> None:
        """Set the changelog template by name."""
        if template_name in self.DEFAULT_TEMPLATES:
            self._template = self.DEFAULT_TEMPLATES[template_name]
            logging.info(f"Using template: {self._template.name}")
        else:
            logging.warning(f"Unknown template '{template_name}', using generic")
            self._template = self.DEFAULT_TEMPLATES["generic"]

    def create_custom_template(
        self,
        name: str,
        project_type: str,
        sections: List[str],
        header_format: str = "## [{version}] - {date}",
        include_links: bool = True,
        include_contributors: bool = False,
    ) -> ChangelogTemplate:
        """Create a custom changelog template."""
        template = ChangelogTemplate(
            name=name,
            project_type=project_type,
            sections=sections,
            header_format=header_format,
            include_links=include_links,
            include_contributors=include_contributors,
        )
        self._template = template
        return template

    def get_template_sections(self) -> List[str]:
        """Get the sections for the current template."""
        if hasattr(self, "_template") and self._template:
            return self._template.sections
        return ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
