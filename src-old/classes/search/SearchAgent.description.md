# SearchAgent

**File**: `src\classes\search\SearchAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 181  
**Complexity**: 8 (moderate)

## Overview

Agent for performing web searches and deep research.

## Classes (1)

### `SearchAgent`

**Inherits from**: BaseAgent

Agent that specializes in researching topics via web search.

**Methods** (8):
- `__init__(self, context)`
- `_get_default_content(self)`
- `_record(self, provider, query, result)`
- `_search_duckduckgo(self, query, max_results)`
- `_search_bing(self, query, max_results)`
- `_search_google(self, query, max_results)`
- `perform_search(self, query)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (14):
- `SearchCore.SearchCore`
- `__future__.annotations`
- `duckduckgo_search.DDGS`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Optional`

---
*Auto-generated documentation*
