#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextCompressor.description.md

# ContextCompressor

**File**: `src\classes\context\ContextCompressor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 2 (simple)

## Overview

Shell for ContextCompressorCore, handling File I/O and orchestration.

## Classes (1)

### `ContextCompressor`

Reduces the size of source files while preserving structural context.

Acts as the I/O Shell for ContextCompressorCore.

**Methods** (2):
- `__init__(self, workspace_root)`
- `compress_file(self, file_path_raw)`

## Dependencies

**Imports** (7):
- `logging`
- `pathlib.Path`
- `src.classes.context.ContextCompressorCore.ContextCompressorCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextCompressor.improvements.md

# Improvements for ContextCompressor

**File**: `src\classes\context\ContextCompressor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextCompressor_test.py` with pytest tests

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

"""Shell for ContextCompressorCore, handling File I/O and orchestration."""

import logging
from pathlib import Path
from typing import Any, Optional

from src.classes.context.ContextCompressorCore import ContextCompressorCore


class ContextCompressor:
    """Reduces the size of source files while preserving structural context.
    
    Acts as the I/O Shell for ContextCompressorCore.
    """

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root: Optional[Path] = Path(workspace_root) if workspace_root else None
        self.core = ContextCompressorCore()

    def compress_file(self, file_path_raw: Any) -> str:
        """Determines compression strategy based on file extension and handles I/O."""
        file_path = Path(file_path_raw)

        if not file_path.exists():
            return f"Error: File {file_path} not found."

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            mode = self.core.decide_compression_mode(file_path.name)
            header = self.core.get_summary_header(file_path.name, mode.capitalize())

            if mode == "python":
                return header + self.core.compress_python(content)
            elif mode == "markdown":
                return header + self.core.summarize_markdown(content)
            else:
                # For other files, just return the first 20 lines
                lines = content.splitlines()[:20]
                return header + "\n".join(lines)
        except Exception as e:
            logging.error(f"Failed to compress {file_path}: {e}")
            return f"Error compressing {file_path.name}: {str(e)}"

if __name__ == "__main__":
    # Test
    compressor = ContextCompressor()
    # Simple self-test
    print(compressor.compress_file(__file__))
