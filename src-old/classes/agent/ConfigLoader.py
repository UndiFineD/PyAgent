#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/ConfigLoader.description.md

# ConfigLoader

**File**: `src\\classes\agent\\ConfigLoader.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 178  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ConfigLoader`

Loads agent configuration from YAML / TOML / JSON files.

Supports multiple configuration file formats and provides
validation and merging of configuration options.

Attributes:
    config_path: Path to configuration file.
    format: Configuration file format.

**Methods** (5):
- `__init__(self, config_path)`
- `load(self)`
- `_parse_content(self, content)`
- `_build_config(self, data)`
- `find_config_file(repo_root)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentConfig.AgentConfig`
- `src.core.base.models.AgentPluginConfig`
- `src.core.base.models.ConfigFormat`
- `src.core.base.models.RateLimitConfig`
- `src.core.base.version.VERSION`
- `toml`
- `tomllib`
- `typing.Any`
- `typing.Optional`
- `typing.cast`
- `yaml`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/ConfigLoader.improvements.md

# Improvements for ConfigLoader

**File**: `src\\classes\agent\\ConfigLoader.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 178 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConfigLoader_test.py` with pytest tests

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


r"""Auto-extracted class from agent.py"""
