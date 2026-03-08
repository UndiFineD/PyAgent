# ExcelAgent

**File**: `src\classes\specialized\ExcelAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 92  
**Complexity**: 4 (simple)

## Overview

Agent specializing in structured extraction from Excel files (ExStruct pattern).

## Classes (1)

### `ExcelAgent`

**Inherits from**: BaseAgent

Parses Excel workbooks into structured JSON (tables, shapes, charts).

**Methods** (4):
- `__init__(self, file_path)`
- `extract_structured_data(self, excel_path, mode)`
- `generate_markdown_summary(self, extraction_result)`
- `improve_content(self, task)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `openpyxl`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
