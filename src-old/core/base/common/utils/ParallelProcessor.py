#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/common/utils/ParallelProcessor.description.md

# ParallelProcessor

**File**: `src\core\base\common\utils\ParallelProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 71  
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

**Imports** (10):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `concurrent.futures.ThreadPoolExecutor`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `tqdm.tqdm`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/common/utils/ParallelProcessor.improvements.md

# Improvements for ParallelProcessor

**File**: `src\core\base\common\utils\ParallelProcessor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 71 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ParallelProcessor_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

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


from src.core.base.version import VERSION
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Any
from collections.abc import Callable

__version__ = VERSION

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class ParallelProcessor:
    """Handles concurrent and parallel execution of tasks across files."""

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers

    def process_files_threaded(
        self, files: list[Path], worker_func: Callable[[Path], Any]
    ) -> list[Any]:
        """Process files using worker threads."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                results = list(
                    tqdm(
                        executor.map(worker_func, files),
                        total=len(files),
                        desc="Processing (Threads)",
                    )
                )
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(
        self, files: list[Path], worker_func: Callable[[Path], Any]
    ) -> list[Any]:
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
