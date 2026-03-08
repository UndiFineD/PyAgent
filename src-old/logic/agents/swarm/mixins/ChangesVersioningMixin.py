#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/mixins/ChangesVersioningMixin.description.md

# ChangesVersioningMixin

**File**: `src\logic\agents\swarm\mixins\ChangesVersioningMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 68  
**Complexity**: 3 (simple)

## Overview

Versioning logic for ChangesAgent.

## Classes (1)

### `ChangesVersioningMixin`

Mixin for managing versioning strategies.

**Methods** (3):
- `set_versioning_strategy(self, strategy)`
- `generate_next_version(self, bump_type)`
- `_extract_latest_version(self)`

## Dependencies

**Imports** (5):
- `VersioningStrategy.VersioningStrategy`
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `re`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/mixins/ChangesVersioningMixin.improvements.md

# Improvements for ChangesVersioningMixin

**File**: `src\logic\agents\swarm\mixins\ChangesVersioningMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ChangesVersioningMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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
Versioning logic for ChangesAgent.
"""

import logging
import re
from datetime import datetime
from ..VersioningStrategy import VersioningStrategy


class ChangesVersioningMixin:
    """Mixin for managing versioning strategies."""

    def set_versioning_strategy(self, strategy: VersioningStrategy) -> None:
        """Set the versioning strategy."""
        self._versioning_strategy = strategy
        logging.info(f"Using versioning strategy: {strategy.value}")

    def generate_next_version(self, bump_type: str = "patch") -> str:
        """Generate the next version based on the current strategy.

        Args:
            bump_type: For SemVer: 'major', 'minor', 'patch'. For CalVer: ignored.
        """
        if self._versioning_strategy == VersioningStrategy.CALVER:
            return datetime.now().strftime("%Y.%m.%d")

        # SemVer: Try to extract current version and bump it
        current_version = self._extract_latest_version()
        if current_version:
            parts = current_version.split(".")
            if len(parts) >= 3:
                try:
                    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                    if bump_type == "major":
                        return f"{major + 1}.0.0"
                    elif bump_type == "minor":
                        return f"{major}.{minor + 1}.0"
                    else:
                        # patch
                        return f"{major}.{minor}.{patch + 1}"
                except ValueError:
                    pass
        return "0.1.0"  # Default starting version

    def _extract_latest_version(self) -> str | None:
        """Extract the latest version from the changelog."""
        if not hasattr(self, "previous_content") or not self.previous_content:
            return None
        pattern = r"##\s*\[?(\d+\.\d+\.\d+)\]?"
        matches = re.findall(pattern, self.previous_content)
        if matches:
            return matches[0]
        return None
