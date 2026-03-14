#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/MCPConnector.description.md

# MCPConnector

**File**: `src\\classes\fleet\\MCPConnector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 117  
**Complexity**: 6 (moderate)

## Overview

Low-level connector for Model Context Protocol (MCP) servers using stdio transport.

## Classes (1)

### `MCPConnector`

Manages the lifecycle and JSON-RPC communication with an MCP server.

**Methods** (6):
- `__init__(self, name, command, env, recorder)`
- `_record(self, action, result)`
- `start(self)`
- `_read_stderr(self)`
- `call(self, method, params, timeout)`
- `stop(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.version.VERSION`
- `subprocess`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/MCPConnector.improvements.md

# Improvements for MCPConnector

**File**: `src\\classes\fleet\\MCPConnector.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 117 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MCPConnector_test.py` with pytest tests

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


r"""Low-level connector for Model Context Protocol (MCP) servers using stdio transport."""
