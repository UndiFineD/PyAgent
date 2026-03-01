# WebCore

**File**: `src\classes\specialized\WebCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 70  
**Complexity**: 2 (simple)

## Overview

WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.

## Classes (1)

### `WebCore`

Pure logic core for Web navigation and extraction.

**Methods** (2):
- `clean_html(html_content)`
- `extract_links(html_content, base_url)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `bs4.BeautifulSoup`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
