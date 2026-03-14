#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/observability/StructuredLogger.description.md

# StructuredLogger

**File**: `src\observability\StructuredLogger.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 178  
**Complexity**: 10 (moderate)

## Overview

StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.

## Classes (1)

### `StructuredLogger`

JSON logger for PyAgent swarm observability.
Phase 277: Added log hygiene with automated GZIP compression.

**Methods** (10):
- `__init__(self, agent_id, trace_id, log_file)`
- `_ensure_log_dir(self)`
- `_compress_logs(self)`
- `_mask_sensitive(self, text)`
- `log(self, level, message)`
- `info(self, message)`
- `error(self, message)`
- `warning(self, message)`
- `debug(self, message)`
- `success(self, message)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `datetime.datetime`
- `datetime.timezone`
- `gzip`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `rust_core`
- `shutil`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/observability/StructuredLogger.improvements.md

# Improvements for StructuredLogger

**File**: `src\observability\StructuredLogger.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 178 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StructuredLogger_test.py` with pytest tests

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
StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.
"""

import gzip
import json
import logging
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.core.base.Version import VERSION

# Rust acceleration for hot-path logging
try:
    import rust_core as rc

    _RUST_ACCEL = True
except ImportError:
    rc = None  # type: ignore[assignment]
    _RUST_ACCEL = False

__version__ = VERSION


class StructuredLogger:
    """
    """
