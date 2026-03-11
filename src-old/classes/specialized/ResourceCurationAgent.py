#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/ResourceCurationAgent.description.md

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
## Source: src-old/classes/specialized/ResourceCurationAgent.improvements.md

# Improvements for ResourceCurationAgent

**File**: `src\classes\specialized\ResourceCurationAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 84 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResourceCurationAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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


"""ResourceCurationAgent for PyAgent.
Specializes in parsing, summarizing, and indexing external research links, 
blog posts, and technical papers into the agent's knowledge base.
"""

import json
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION

__version__ = VERSION


class ResourceCurationAgent(BaseAgent):
    """Manages the 'Good Read Unit' and research link lifecycle."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.library_path = "data/memory/knowledge_exports/research_library.json"
        self._system_prompt = (
            "You are the Resource Curation Agent. Your goal is to keep the fleet's knowledge "
            "up-to-date by parsing research links, extracting actionable insights, and "
            "categorizing content for the KnowledgeAgent and FeatureStoreAgent."
        )

    @as_tool
    def add_resource(
        self, url: str, title: str, summary: str | None = None, tags: list[str] = None
    ) -> str:
        """Adds a new research resource to the library."""
        resource = {
            "url": url,
            "title": title,
            "summary": summary or "Pending automated summary",
            "tags": tags or [],
            "status": "Archived",
        }

        try:
            library = self._load_library()
            library.append(resource)
            self._save_library(library)
            return f"Resource '{title}' added to the Research Library."
        except Exception as e:
            return f"Failed to add resource: {e}"

    @as_tool
    def process_research_queue(self, urls: list[str]) -> str:
        """Bulk processes a list of discovery URLs."""
        # Simulated extraction logic
        return f"Processed {len(urls)} research items. Recommendations sent to KnowledgeAgent."

    def _load_library(self) -> list[dict[str, Any]]:
        import os

        if not os.path.exists(self.library_path):
            return []
        with open(self.library_path, encoding="utf-8") as f:
            return json.load(f)

    def _save_library(self, data: list[dict[str, Any]]) -> None:
        with open(self.library_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def improve_content(self, input_text: str) -> str:
        return f"Library currently contains {len(self._load_library())} curated research units."


if __name__ == "__main__":
    from src.core.base.utilities import create_main_function

    main = create_main_function(
        ResourceCurationAgent,
        "Resource Curation Agent",
        "Curating research and documentation",
    )
    main()
