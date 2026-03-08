# browser_agent

**File**: `src\logic\agents\browser\browser_agent.py`  
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
