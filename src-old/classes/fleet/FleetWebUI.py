#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/FleetWebUI.description.md

# FleetWebUI

**File**: `src\\classes\fleet\\FleetWebUI.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 145  
**Complexity**: 10 (moderate)

## Overview

Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.

## Classes (1)

### `FleetWebUI`

Provides backend support for the Fleet visualization dashboard.

**Methods** (10):
- `__init__(self, fleet_manager)`
- `register_generative_component(self, name, description, props_schema)`
- `suggest_ui_components(self, task_result)`
- `get_fleet_topology(self)`
- `generate_workflow_graph(self, workflow_state)`
- `get_metrics_snapshot(self)`
- `list_workspace_files(self, sub_path)`
- `_get_preview(self, file_path)`
- `get_workflow_designer_state(self)`
- `get_multi_fleet_manager(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/FleetWebUI.improvements.md

# Improvements for FleetWebUI

**File**: `src\\classes\fleet\\FleetWebUI.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 145 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FleetWebUI_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.
"""
import json
import logging
from pathlib import Path
from typing import Any

from src.core.base.version import VERSION

__version__ = VERSION


class FleetWebUI:
    """
    """
