# file_classifier

**File**: `src\logic\agents\forensics\file_classifier.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 255  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for file_classifier.

## Classes (2)

### `FileAnalysisResult`

Class FileAnalysisResult implementation.

### `FileClassifier`

Analyzes files to determine type, calculate hashes, and identify suspicious content.
Ported concepts from 0xSojalSec-Catalyzer and 0xSojalSec-CanaryTokenScanner.

**Methods** (3):
- `__init__(self)`
- `_load_signatures(self)`
- `_extract_and_scan_sync(self, path)`

## Dependencies

**Imports** (15):
- `aiofiles`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `hashlib`
- `json`
- `pathlib.Path`
- `re`
- `shutil`
- `tempfile`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `zipfile`

---
*Auto-generated documentation*
