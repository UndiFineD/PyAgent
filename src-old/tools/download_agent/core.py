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

## Source: src-old/tools/download_agent/core.description.md

# core

**File**: `src\tools\\download_agent\\core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 350  
**Complexity**: 10 (moderate)

## Overview

Core download agent functionality.

## Classes (1)

### `DownloadAgent`

Main download agent that handles different URL types.

**Methods** (10):
- `__init__(self, config)`
- `ensure_directory(self, path)`
- `download_github_repo(self, url, metadata)`
- `download_github_gist(self, url, metadata)`
- `download_file(self, url, metadata, filename)`
- `download_arxiv_paper(self, url, metadata)`
- `open_webpage(self, url, metadata)`
- `process_url(self, url)`
- `process_urls_file(self)`
- `save_results(self, results, output_file)`

## Dependencies

**Imports** (14):
- `classifiers.URLClassifier`
- `datetime.datetime`
- `json`
- `models.DownloadConfig`
- `models.DownloadResult`
- `os`
- `pathlib.Path`
- `requests`
- `subprocess`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
## Source: src-old/tools/download_agent/core.improvements.md

# Improvements for core

**File**: `src\tools\\download_agent\\core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 350 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `core_test.py` with pytest tests

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
Core download agent functionality.
"""
import json
import os
import subprocess
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests

from .classifiers import URLClassifier
from .models import DownloadConfig, DownloadResult


class DownloadAgent:
    """
    """
