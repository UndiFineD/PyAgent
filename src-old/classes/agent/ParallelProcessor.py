#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent/ParallelProcessor.description.md

# ParallelProcessor

**File**: `src\\classes\agent\\ParallelProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 55  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ParallelProcessor.

## Classes (1)

### `ParallelProcessor`

Handles concurrent and parallel execution of tasks across files.

**Methods** (2):
- `__init__(self, max_workers)`
- `process_files_threaded(self, files, worker_func)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `functools`
- `logging`
- `pathlib.Path`
- `tqdm.tqdm`
- `typing.Any`
- `typing.Callable`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/ParallelProcessor.improvements.md

# Improvements for ParallelProcessor

**File**: `src\\classes\agent\\ParallelProcessor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 55 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ParallelProcessor_test.py` with pytest tests

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

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, List

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class ParallelProcessor:
    """Handles concurrent and parallel execution of tasks across files."""

    def __init__(self, max_workers: int = 4) -> None:
        """Initialize the ParallelProcessor with a maximum number of worker threads."""
        self.max_workers = max_workers

    def process_files_threaded(
        self, files: List[Path], worker_func: Callable[[Path], Any]
    ) -> List[Any]:
        """Process files using worker threads."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                # Ensure tqdm is available before using it
                mapped_results = executor.map(worker_func, files)
                results = list(tqdm(mapped_results, total=len(files), desc="Processing (Threads)"))
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(
        self, files: List[Path], worker_func: Callable[[Path], Any]
    ) -> List[Any]:
        """Process multiple files concurrently using async/await."""
        modified_results: list[Any] = []
        loop = asyncio.get_running_loop()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:

            async def wrap_worker(file_path: Path) -> None:
                try:
                    res = await loop.run_in_executor(executor, worker_func, file_path)
                    if res:
                        modified_results.append(res)
                except Exception as e:
                    logging.error(f"[async] Failed to process {file_path.name}: {e}")

            tasks = [wrap_worker(f) for f in files]
            if tasks:
                await asyncio.gather(*tasks)

        return modified_results
