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

"""
LLM_CONTEXT_START

## Source: src-old/tools/download_agent/models.description.md

# models

**File**: `src\tools\download_agent\models.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 2 imports  
**Lines**: 45  
**Complexity**: 0 (simple)

## Overview

Data models for the Download Agent.

## Classes (2)

### `DownloadResult`

Result of a download operation.

### `DownloadConfig`

Configuration for download operations.

## Dependencies

**Imports** (2):
- `dataclasses.dataclass`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/tools/download_agent/models.improvements.md

# Improvements for models

**File**: `src\tools\download_agent\models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `models_test.py` with pytest tests

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

"""
Data models for the Download Agent.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class DownloadResult:
    """Result of a download operation."""

    url: str
    success: bool
    destination: str
    file_type: str
    size_bytes: int = 0
    error_message: str = ""
    metadata: Dict = None


@dataclass
class DownloadConfig:
    """Configuration for download operations."""

    urls_file: str = "docs/download/urls.txt"
    base_dir: str = "."
    max_retries: int = 3
    timeout_seconds: int = 30
    delay_between_downloads: float = 1.0
    skip_existing: bool = True
    dry_run: bool = False
    verbose: bool = False
