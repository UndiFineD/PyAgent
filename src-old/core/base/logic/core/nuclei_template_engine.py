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

## Source: src-old/core/base/logic/core/nuclei_template_engine.description.md

# nuclei_template_engine

**File**: `src\\core\base\\logic\\core\nuclei_template_engine.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 13 imports  
**Lines**: 425  
**Complexity**: 10 (moderate)

## Overview

Nuclei-style Vulnerability Template Engine

Inspired by Nuclei templates from .external/0day-templates repository.
Implements YAML-based vulnerability detection templates with DSL matchers.

## Classes (7)

### `TemplateInfo`

Template metadata

### `TemplateRequest`

HTTP request specification

### `MatcherCondition`

Matcher condition specification

### `TemplateHTTP`

HTTP template specification

### `NucleiTemplate`

Complete Nuclei template

### `ScanResult`

Result from template execution

### `NucleiTemplateEngine`

Nuclei-style vulnerability detection engine.

Based on patterns from .external/0day-templates repository.

**Methods** (10):
- `__init__(self)`
- `load_template_from_yaml(self, yaml_content)`
- `load_template_from_file(self, file_path)`
- `_build_url(self, base_url, path)`
- `_check_matchers(self, matchers, response, condition)`
- `_check_single_matcher(self, matcher, response)`
- `_check_dsl_matcher(self, dsl_expressions, response)`
- `_check_word_matcher(self, words, content)`
- `_check_regex_matcher(self, patterns, content)`
- `get_available_templates(self)`

## Dependencies

**Imports** (13):
- `asyncio`
- `dataclasses.dataclass`
- `logging`
- `pathlib.Path`
- `re`
- `requests`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`
- `urllib.parse.urlparse`
- `yaml`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/nuclei_template_engine.improvements.md

# Improvements for nuclei_template_engine

**File**: `src\\core\base\\logic\\core\nuclei_template_engine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 425 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `nuclei_template_engine_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

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
Nuclei-style Vulnerability Template Engine

Inspired by Nuclei templates from .external/0day-templates repository.
Implements YAML-based vulnerability detection templates with DSL matchers.
"""
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
import yaml


@dataclass
class TemplateInfo:
    """
    """
