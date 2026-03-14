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

## Source: src-old/logic/tools/nuclei/template_collector.description.md

# template_collector

**File**: `src\\logic\tools\nuclei\template_collector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 131  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for template_collector.

## Classes (1)

### `NucleiTemplateCollector`

Collects Nuclei templates from various public repositories.
Adapted from AllForOne tool.

**Methods** (5):
- `__init__(self, output_dir)`
- `_git_clone(self, url, destination)`
- `_generate_destination_folder(self, url)`
- `_clone_repository(self, repo)`
- `collect_templates(self, source_url)`

## Dependencies

**Imports** (7):
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.wait`
- `logging`
- `os`
- `requests`
- `shutil`
- `subprocess`

---
*Auto-generated documentation*
## Source: src-old/logic/tools/nuclei/template_collector.improvements.md

# Improvements for template_collector

**File**: `src\\logic\tools\nuclei\template_collector.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `template_collector_test.py` with pytest tests

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
import logging
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, wait

import requests

logger = logging.getLogger(__name__)


class NucleiTemplateCollector:
    """
    """
