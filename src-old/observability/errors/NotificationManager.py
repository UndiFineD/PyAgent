#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/observability/errors/NotificationManager.description.md

# NotificationManager

**File**: `src\observability\errors\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 101  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_errors.py

## Classes (1)

### `NotificationManager`

Manages error notifications to various channels.

Supports Slack, Teams, Email, Webhooks, and Discord notifications
with configurable severity thresholds.

Attributes:
    configs: List of notification configurations.

**Methods** (7):
- `__init__(self)`
- `add_config(self, config)`
- `remove_config(self, channel)`
- `notify(self, error)`
- `_format_message(self, error, template)`
- `_send(self, config, message)`
- `get_configs(self)`

## Dependencies

**Imports** (7):
- `ErrorEntry.ErrorEntry`
- `NotificationChannel.NotificationChannel`
- `NotificationConfig.NotificationConfig`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/errors/NotificationManager.improvements.md

# Improvements for NotificationManager

**File**: `src\observability\errors\NotificationManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NotificationManager_test.py` with pytest tests

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


r"""Auto-extracted class from agent_errors.py"""
