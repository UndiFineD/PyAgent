# ReportGenerator

**File**: `src\classes\reports\ReportGenerator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 20 imports  
**Lines**: 446  
**Complexity**: 25 (complex)

## Overview

Report generation logic for agent source files.

## Classes (1)

### `ReportGenerator`

Generates quality reports (description, errors, improvements) for agent files.

**Methods** (25):
- `__init__(self, agent_dir, output_dir, recorder)`
- `_record(self, action, result)`
- `process_all_files(self)`
- `export_jsonl_report(self, items, filename)`
- `generate_full_report(self)`
- `render_3x3_grid(self)`
- `process_file(self, py_path)`
- `iter_agent_py_files(self)`
- `render_description(self, py_path, source, tree)`
- `render_errors(self, py_path, source, compile_result)`
- ... and 15 more methods

## Dependencies

**Imports** (20):
- `CompileResult.CompileResult`
- `__future__.annotations`
- `ast`
- `collections.abc.Iterable`
- `core.DeduplicationCore.DeduplicationCore`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `time`
- `typing.Any`
- ... and 5 more

---
*Auto-generated documentation*
