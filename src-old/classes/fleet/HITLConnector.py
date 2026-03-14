#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/HITLConnector.description.md

# HITLConnector

**File**: `src\\classes\fleet\\HITLConnector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 98  
**Complexity**: 4 (simple)

## Overview

Human-in-the-loop (HITL) connector for fleet approvals.
Supports Slack and Discord notification patterns for critical agent decisions.

## Classes (1)

### `HITLConnector`

Manages external communication with humans for high-stakes approvals.

**Methods** (4):
- `__init__(self, webhook_url, workspace_root)`
- `request_approval(self, agent_id, task, context)`
- `check_approval_status(self, approval_id)`
- `get_pending_summary(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/HITLConnector.improvements.md

# Improvements for HITLConnector

**File**: `src\\classes\fleet\\HITLConnector.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 98 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HITLConnector_test.py` with pytest tests

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


"""Human-in-the-loop (HITL) connector for fleet approvals.
Supports Slack and Discord notification patterns for critical agent decisions.
"""
import logging
import time
import urllib.parse
from pathlib import Path
from typing import Any

from src.core.base.ConnectivityManager import ConnectivityManager
from src.core.base.version import VERSION
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

# Infrastructure
__version__ = VERSION


class HITLConnector:
    """
    """
