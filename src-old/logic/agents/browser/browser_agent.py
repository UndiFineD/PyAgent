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

## Source: src-old/logic/agents/browser/browser_agent.description.md

# browser_agent

**File**: `src\\logic\agents\browser\browser_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 308  
**Complexity**: 12 (moderate)

## Overview

Browser Agent - Web automation and information extraction
========================================================

Inspired by big-3-super-agent's GeminiBrowserAgent.
Provides web browsing capabilities with screenshot capture and interaction.

## Classes (1)

### `BrowserAgent`

**Inherits from**: BaseAgent

Web browser automation agent inspired by big-3-super-agent.

Features:
- Playwright-based browser control
- Screenshot capture and management
- Web page interaction and data extraction
- Session-based organization

**Methods** (12):
- `__init__(self)`
- `setup_browser(self)`
- `cleanup_browser(self)`
- `take_screenshot(self, description)`
- `navigate_to_url(self, url, wait_until)`
- `extract_text_content(self)`
- `search_on_page(self, query)`
- `click_element(self, selector)`
- `fill_form(self, selector, value)`
- `scroll_page(self, direction, amount)`
- ... and 2 more methods

## Dependencies

**Imports** (16):
- `asyncio`
- `datetime.datetime`
- `logging`
- `os`
- `pathlib.Path`
- `playwright.sync_api.Page`
- `playwright.sync_api.sync_playwright`
- `rich.console.Console`
- `rich.panel.Panel`
- `src.core.base.base_agent.BaseAgent`
- `src.core.base.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
## Source: src-old/logic/agents/browser/browser_agent.improvements.md

# Improvements for browser_agent

**File**: `src\\logic\agents\browser\browser_agent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 308 lines (medium)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `browser_agent_test.py` with pytest tests

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
Browser Agent - Web automation and information extraction
========================================================

Inspired by big-3-super-agent's GeminiBrowserAgent.
Provides web browsing capabilities with screenshot capture and interaction.
"""
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from playwright.sync_api import sync_playwright
from rich.console import Console
from src.core.base.base_agent import BaseAgent
from src.core.base.models.communication_models import CascadeContext


class BrowserAgent(BaseAgent):
    """
    """
