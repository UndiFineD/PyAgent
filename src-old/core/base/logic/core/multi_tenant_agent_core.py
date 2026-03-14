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

## Source: src-old/core/base/logic/core/multi_tenant_agent_core.description.md

# multi_tenant_agent_core

**File**: `src\\core\base\\logic\\core\\multi_tenant_agent_core.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 14 imports  
**Lines**: 560  
**Complexity**: 1 (simple)

## Overview

Multi-Tenant Agent Core

Implements multi-tenant agent orchestration patterns from AgentCloud.
Provides database-driven agent, task, and crew management with resource controls.
Based on AgentCloud's CrewAI platform architecture.

## Classes (11)

### `ProcessType`

**Inherits from**: str, Enum

Crew process types.

### `ToolType`

**Inherits from**: str, Enum

Tool types supported.

### `AgentStatus`

**Inherits from**: str, Enum

Agent status states.

### `TaskStatus`

**Inherits from**: str, Enum

Task execution status.

### `TenantConfig`

Configuration for a tenant.

### `AgentDefinition`

Agent definition with role and capabilities.

### `TaskDefinition`

Task definition with requirements and outputs.

### `CrewDefinition`

Crew definition for multi-agent orchestration.

### `ToolDefinition`

Tool definition with capabilities.

### `ExecutionResult`

Result of task/crew execution.

### `MultiTenantAgentCore`

**Inherits from**: BaseCore

Multi-tenant agent orchestration core based on AgentCloud patterns.

Features:
- Tenant isolation with resource limits
- Database-driven agent/task/crew management
- Multiple process types (sequential, hierarchical, consensual)
- Tool management and assignment
- Rate limiting and resource controls
- Execution tracking and monitoring

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (14):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/multi_tenant_agent_core.improvements.md

# Improvements for multi_tenant_agent_core

**File**: `src\\core\base\\logic\\core\\multi_tenant_agent_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 560 lines (large)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `multi_tenant_agent_core_test.py` with pytest tests

### Code Organization
- [TIP] **11 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (560 lines) - Consider refactoring

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
Multi-Tenant Agent Core

Implements multi-tenant agent orchestration patterns from AgentCloud.
Provides database-driven agent, task, and crew management with resource controls.
Based on AgentCloud's CrewAI platform architecture.
"""
import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from src.core.base.common.base_core import BaseCore


class ProcessType(str, Enum):
    """
    """
