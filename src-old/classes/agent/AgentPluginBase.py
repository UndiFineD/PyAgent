#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent/AgentPluginBase.description.md

# AgentPluginBase

**File**: `src\\classes\agent\\AgentPluginBase.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 89  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `AgentPluginBase`

**Inherits from**: ABC

Abstract base class for agent plugins.

Provides interface for third - party agents to integrate with
the agent orchestrator without modifying core code.

Attributes:
    name: Plugin name.
    priority: Execution priority.
    config: Plugin configuration.

**Methods** (6):
- `__init__(self, name, priority, config)`
- `run(self, file_path, context)`
- `setup(self)`
- `shutdown(self)`
- `teardown(self)`
- `health_check(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.HealthStatus`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/AgentPluginBase.improvements.md

# Improvements for AgentPluginBase

**File**: `src\\classes\agent\\AgentPluginBase.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 89 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentPluginBase_test.py` with pytest tests

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


"""Auto-extracted class from agent.py"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.core.base.models import AgentHealthCheck, AgentPriority, HealthStatus
from src.core.base.version import VERSION

__version__ = VERSION


class AgentPluginBase(ABC):
    """Abstract base class for agent plugins.

    Provides interface for third - party agents to integrate with
    the agent orchestrator without modifying core code.

    Attributes:
        name: Plugin name.
        priority: Execution priority.
        config: Plugin configuration.

    """

    def __init__(
        self,
        name: str,
        priority: AgentPriority = AgentPriority.NORMAL,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the plugin.

        Args:
            name: Unique plugin name.
            priority: Execution priority.
            config: Plugin - specific configuration.

        """
        self.name = name
        self.priority = priority
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{name}")

    @abstractmethod
    def run(self, file_path: Path, context: dict[str, Any]) -> bool:
        """Execute the plugin on a file.

        Args:
            file_path: Path to the file to process.
            context: Execution context with agent state.

        Returns:
            bool: True if changes were made, False otherwise.

        """
        raise NotImplementedError()

    def setup(self) -> None:
        """Called once when plugin is loaded. Override for initialization."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Handle graceful shutdown, cleanup resources, and terminate processes."""
        raise NotImplementedError()

    def teardown(self) -> None:
        """Called once when plugin is unloaded. Override for cleanup."""
        pass

    def health_check(self) -> AgentHealthCheck:
        """Check plugin health status.

        Returns:
            AgentHealthCheck: Health check result.

        """
        return AgentHealthCheck(agent_name=self.name, status=HealthStatus.HEALTHY)
