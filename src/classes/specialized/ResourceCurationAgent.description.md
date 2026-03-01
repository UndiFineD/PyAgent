# ResourceCurationAgent

**File**: `src\classes\specialized\ResourceCurationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 84  
**Complexity**: 6 (moderate)

## Overview

ResourceCurationAgent for PyAgent.
Specializes in parsing, summarizing, and indexing external research links, 
blog posts, and technical papers into the agent's knowledge base.

## Classes (1)

### `ResourceCurationAgent`

**Inherits from**: BaseAgent

Manages the 'Good Read Unit' and research link lifecycle.

**Methods** (6):
- `__init__(self, file_path)`
- `add_resource(self, url, title, summary, tags)`
- `process_research_queue(self, urls)`
- `_load_library(self)`
- `_save_library(self, data)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `json`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
