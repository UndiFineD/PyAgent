# fix_headers_agent

**File**: `src\maintenance\fix_headers\fix_headers_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 7 imports  
**Lines**: 286  
**Complexity**: 9 (moderate)

## Overview

Fix Headers Agent for PyAgent.

This agent ensures all Python files have proper Apache 2.0 license headers
and copyright notices. It can process individual files or entire directory
trees, making it useful for maintaining code quality across the PyAgent fleet.

## Classes (1)

### `FixHeadersAgent`

Agent for fixing and standardizing license headers in Python files.

This agent ensures all Python files in the PyAgent codebase have consistent
Apache 2.0 license headers with proper copyright notices. It can process
individual files, directories, or entire project trees.

**Methods** (8):
- `__init__(self, dry_run, verbose)`
- `has_proper_header(self, content)`
- `clean_existing_headers(self, content)`
- `add_header(self, content)`
- `process_file(self, filepath)`
- `process_directory(self, directory, exclude_patterns)`
- `get_summary(self)`
- `run(self, target, exclude_patterns)`

## Functions (1)

### `main()`

CLI entry point for the Fix Headers Agent.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `argparse`
- `os`
- `pathlib.Path`
- `re`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
