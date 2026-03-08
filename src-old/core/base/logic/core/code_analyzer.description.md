# code_analyzer

**File**: `src\core\base\logic\core\code_analyzer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 96  
**Complexity**: 4 (simple)

## Overview

Core code analysis logic regarding API summarization and structural inspection.
Inspired by Feathr (ai-eng) source code compacting.

## Classes (1)

### `CodeAnalyzerCore`

Core logic regarding extracting compact API representations from source code.

**Methods** (4):
- `__init__(self, workspace_root)`
- `generate_compact_guide(self, path)`
- `_summarize_file(self, file_path)`
- `calculate_metrics_summary(self, source)`

## Dependencies

**Imports** (7):
- `ast`
- `os`
- `pathlib.Path`
- `re`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
