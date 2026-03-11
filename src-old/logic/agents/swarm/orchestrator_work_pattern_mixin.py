#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/orchestrator_work_pattern_mixin.description.md

# orchestrator_work_pattern_mixin

**File**: `src\\logic\agents\\swarm\\orchestrator_work_pattern_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 121  
**Complexity**: 5 (moderate)

## Overview

OrchestratorWorkPatternMixin: Mixin for work pattern orchestration in PyAgent.

## Classes (1)

### `OrchestratorWorkPatternMixin`

Mixin class that provides work pattern orchestration capabilities to OrchestratorAgent.

Enables the orchestrator to execute structured collaborative workflows using
predefined work patterns like PEER (Planning, Executing, Expressing, Reviewing).

**Methods** (5):
- `__init__(self)`
- `register_work_pattern(self, pattern)`
- `get_work_pattern(self, name)`
- `list_work_patterns(self)`
- `validate_work_pattern_setup(self, pattern_name)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.work_patterns.WorkPattern`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/orchestrator_work_pattern_mixin.improvements.md

# Improvements for orchestrator_work_pattern_mixin

**File**: `src\\logic\agents\\swarm\\orchestrator_work_pattern_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 121 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `orchestrator_work_pattern_mixin_test.py` with pytest tests

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
OrchestratorWorkPatternMixin: Mixin for work pattern orchestration in PyAgent.
"""


import logging
from typing import Any, Dict, Optional

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.work_patterns import WorkPattern

logger = logging.getLogger(__name__)


class OrchestratorWorkPatternMixin:
    """Mixin class that provides work pattern orchestration capabilities to OrchestratorAgent.

    Enables the orchestrator to execute structured collaborative workflows using
    predefined work patterns like PEER (Planning, Executing, Expressing, Reviewing).
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize work pattern capabilities."""
        super().__init__(**kwargs)
        self._work_patterns: Dict[str, WorkPattern] = {}
        self._default_work_pattern: Optional[str] = None

    def register_work_pattern(self, pattern: WorkPattern) -> None:
        """Register a work pattern for use in orchestration.

        Args:
            pattern: The work pattern to register

        """
        self._work_patterns[pattern.name] = pattern
        logger.info(f"Registered work pattern: {pattern.name}")

        # Set as default if it's the first one or named "PEER"
        if self._default_work_pattern is None or pattern.name == "PEER":
            self._default_work_pattern = pattern.name

    def get_work_pattern(self, name: str) -> Optional[WorkPattern]:
        """Get a registered work pattern by name.

        Args:
            name: Name of the work pattern

        Returns:
            The work pattern instance or None if not found

        """
        return self._work_patterns.get(name)

    def list_work_patterns(self) -> list[str]:
        """List all registered work pattern names.

        Returns:
            List of work pattern names

        """
        return list(self._work_patterns.keys())

    async def execute_with_pattern(
        self, context: CascadeContext, pattern_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute a task using a specific work pattern.

        Args:
            context: The cascade context for the task
            pattern_name: Name of the work pattern to use (uses default if None)
            **kwargs: Additional parameters for the pattern

        Returns:
            Results from the work pattern execution

        """
        pattern_name = pattern_name or self._default_work_pattern
        if not pattern_name:
            raise ValueError("No work pattern specified and no default pattern set")

        pattern = self.get_work_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Work pattern '{pattern_name}' not found")

        logger.info(f"Executing task with work pattern: {pattern_name}")
        return await pattern.execute(context, **kwargs)

    def validate_work_pattern_setup(self, pattern_name: str) -> bool:
        """Validate that a work pattern is properly configured.

        Args:
            pattern_name: Name of the work pattern to validate

        Returns:
            True if the pattern is valid and ready to use

        """
        pattern = self.get_work_pattern(pattern_name)
        if not pattern:
            logger.warning(f"Work pattern '{pattern_name}' not found")
            return False

        if not pattern.validate_agents():
            logger.warning(
                f"Work pattern '{pattern_name}' has invalid agent configuration"
            )
            return False

        return True
