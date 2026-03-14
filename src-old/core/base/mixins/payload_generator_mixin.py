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

## Source: src-old/core/base/mixins/payload_generator_mixin.description.md

# payload_generator_mixin

**File**: `src\\core\base\\mixins\\payload_generator_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 168  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for payload_generator_mixin.

## Classes (1)

### `PayloadGeneratorMixin`

Mixin providing payload generation capabilities for various exploits.

Inspired by aem-hacker's hardcoded payloads for SSRF, RCE, XSS, etc.

**Methods** (9):
- `__init__(self)`
- `_load_default_templates(self)`
- `generate_ssrf_rce_payload(self, fake_aem_host)`
- `generate_xss_payload(self, payload_type, index)`
- `generate_deserialization_payload(self, payload_type)`
- `generate_groovy_rce_payload(self, command)`
- `add_payload_template(self, name, template)`
- `get_payload_template(self, name)`
- `list_payload_templates(self)`

## Dependencies

**Imports** (8):
- `base64`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse.quote`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/payload_generator_mixin.improvements.md

# Improvements for payload_generator_mixin

**File**: `src\\core\base\\mixins\\payload_generator_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 168 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `payload_generator_mixin_test.py` with pytest tests

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
import base64
import uuid
from typing import Any, Dict, List, Optional
from urllib.parse import quote


class PayloadGeneratorMixin:
    """
    """
