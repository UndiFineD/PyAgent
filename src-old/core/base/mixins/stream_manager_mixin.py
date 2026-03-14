#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/stream_manager_mixin.description.md

# stream_manager_mixin

**File**: `src\\core\base\\mixins\\stream_manager_mixin.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 17 imports  
**Lines**: 320  
**Complexity**: 5 (moderate)

## Overview

Stream Management Mixin for BaseAgent.
Provides Redis-backed streaming capabilities with resumability, adapted from Adorable patterns.

## Classes (3)

### `StreamState`

Represents the current state of a stream.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `StreamInfo`

Information about an active stream.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `StreamManagerMixin`

Mixin providing Redis-backed stream management capabilities.
Adapted from Adorable's stream-manager.ts patterns for Python/asyncio.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `asyncio`
- `contextlib.asynccontextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `logging`
- `redis.asyncio`
- `src.core.base.common.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.AsyncGenerator`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/stream_manager_mixin.improvements.md

# Improvements for stream_manager_mixin

**File**: `src\\core\base\\mixins\\stream_manager_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 320 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `stream_manager_mixin_test.py` with pytest tests

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
Stream Management Mixin for BaseAgent.
Provides Redis-backed streaming capabilities with resumability, adapted from Adorable patterns.
"""
import asyncio
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

try:
    import redis.asyncio as redis
    HAS_REDIS = True
except ImportError:
    redis = None
    HAS_REDIS = False



@dataclass
class StreamState:
    """
    """
