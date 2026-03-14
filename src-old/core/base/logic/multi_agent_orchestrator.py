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

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/multi_agent_orchestrator.description.md

# multi_agent_orchestrator

**File**: `src\\core\base\\logic\\multi_agent_orchestrator.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 17 imports  
**Lines**: 435  
**Complexity**: 13 (moderate)

## Overview

Multi-Agent Orchestrator Core - Unified Agent Management System
=================================================================

Inspired by big-3-super-agent's orchestration patterns, this core provides:
- Unified interface for managing multiple agent types (voice, coding, browser)
- Agent registry with persistent session management
- Tool-based dispatch system for agent orchestration
- Background task processing with status tracking
- Working directory management per agent type

Key Patterns Extracted from big-3-super-agent:
- Agent registry system with session persistence
- Tool-based orchestration via function calls
- Background processing with operator logs
- Multi-agent coordination and lifecycle management

## Classes (3)

### `AgentMetadata`

Metadata for registered agents.

### `TaskResult`

Result of an agent task execution.

### `MultiAgentOrchestratorCore`

Unified orchestrator for managing multiple agent types.

Provides a centralized system for:
- Agent registration and lifecycle management
- Task dispatch and execution tracking
- Working directory management
- Tool-based orchestration interface

**Methods** (13):
- `__init__(self, base_working_dir)`
- `_load_registry(self)`
- `_save_registry(self)`
- `register_agent_type(self, agent_type, handler)`
- `create_agent(self, agent_type, agent_name, capabilities, context)`
- `dispatch_task(self, agent_name, task_description, parameters, context)`
- `get_task_status(self, task_id)`
- `list_agents(self, agent_type)`
- `delete_agent(self, agent_name)`
- `get_agent_tools(self, agent_name)`
- ... and 3 more methods

## Dependencies

**Imports** (17):
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timezone`
- `json`
- `pathlib.Path`
- `shutil`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.state.agent_state_manager.StateTransaction`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/multi_agent_orchestrator.improvements.md

# Improvements for multi_agent_orchestrator

**File**: `src\\core\base\\logic\\multi_agent_orchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 435 lines (medium)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `multi_agent_orchestrator_test.py` with pytest tests

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

"""
Multi-Agent Orchestrator Core - Unified Agent Management System
=================================================================

Inspired by big-3-super-agent's orchestration patterns, this core provides:
- Unified interface for managing multiple agent types (voice, coding, browser)
- Agent registry with persistent session management
- Tool-based dispatch system for agent orchestration
- Background task processing with status tracking
- Working directory management per agent type

Key Patterns Extracted from big-3-super-agent:
- Agent registry system with session persistence
- Tool-based orchestration via function calls
- Background processing with operator logs
- Multi-agent coordination and lifecycle management
"""
import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.state.agent_state_manager import StateTransaction


@dataclass
class AgentMetadata:
    """
    """
