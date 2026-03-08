# MarkdownAgent

**File**: `src\classes\coder\MarkdownAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 151  
**Complexity**: 11 (moderate)

## Overview

Agent specializing in Markdown documentation.

## Classes (1)

### `MarkdownAgent`

**Inherits from**: CoderAgent

Agent for Markdown documentation improvement.

**Methods** (11):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `convert_to_wikilinks(self, content)`
- `format_as_callout(self, content, callout_type, title)`
- `ensure_frontmatter(self, content, default_props)`
- `add_mermaid_diagram(self, diagram_type, diagram_definition)`
- `add_dataview_query(self, query)`
- `insert_knowledge_graph(self)`
- `insert_backlinks(self)`
- `convert_to_callouts(self, content)`
- ... and 1 more methods

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `re`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.KnowledgeAgent.KnowledgeAgent`
- `src.logic.agents.development.CoderAgent.CoderAgent`
- `yaml`

---
*Auto-generated documentation*
