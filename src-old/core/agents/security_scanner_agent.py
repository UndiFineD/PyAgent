#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/agents/security_scanner_agent.description.md

# security_scanner_agent

**File**: `src\\core\agents\\security_scanner_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 169  
**Complexity**: 2 (simple)

## Overview

Module: security_scanner_agent
Agent for comprehensive security scanning using patterns from aem-hacker.
Implements vulnerability scanning, payload generation, SSRF detection, and reconnaissance.

## Classes (1)

### `SecurityScannerAgent`

**Inherits from**: BaseAgent, VulnerabilityScannerMixin, PayloadGeneratorMixin, SSRFDetectorMixin, ReconnaissanceMixin

Comprehensive security scanner agent inspired by aem-hacker patterns.

Features:
- Modular vulnerability scanning with extensible checks
- Payload generation for various exploit types
- SSRF detection using callback server pattern
- Target reconnaissance and service fingerprinting

**Methods** (2):
- `__init__(self)`
- `_generate_scan_summary(self, results)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.mixins.payload_generator_mixin.PayloadGeneratorMixin`
- `src.core.base.mixins.reconnaissance_mixin.ReconnaissanceMixin`
- `src.core.base.mixins.ssrf_detector_mixin.SSRFDetectorMixin`
- `src.core.base.mixins.vulnerability_scanner_mixin.VulnerabilityScannerMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid.UUID`

---
*Auto-generated documentation*
## Source: src-old/core/agents/security_scanner_agent.improvements.md

# Improvements for security_scanner_agent

**File**: `src\\core\agents\\security_scanner_agent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 169 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `security_scanner_agent_test.py` with pytest tests

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
Module: security_scanner_agent
Agent for comprehensive security scanning using patterns from aem-hacker.
Implements vulnerability scanning, payload generation, SSRF detection, and reconnaissance.
"""
from typing import Any, Dict, List

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.mixins.payload_generator_mixin import PayloadGeneratorMixin
from src.core.base.mixins.reconnaissance_mixin import ReconnaissanceMixin
from src.core.base.mixins.ssrf_detector_mixin import SSRFDetectorMixin
from src.core.base.mixins.vulnerability_scanner_mixin import VulnerabilityScannerMixin


class SecurityScannerAgent(
    BaseAgent,
    VulnerabilityScannerMixin,
    PayloadGeneratorMixin,
    SSRFDetectorMixin,
    ReconnaissanceMixin,
):
    """
    """
