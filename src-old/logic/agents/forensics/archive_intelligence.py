#!/usr/bin/env python3
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

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/forensics/archive_intelligence.description.md

# archive_intelligence

**File**: `src\\logic\agents\forensics\archive_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 74  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for archive_intelligence.

## Classes (1)

### `ArchiveIntelligence`

Refactored logic from Archive Alchemist for safe archive analysis.
Focuses on detecting malicious patterns like ZipSlip or massive compression ratios.

## Dependencies

**Imports** (7):
- `os`
- `pathlib.Path`
- `shutil`
- `tarfile`
- `typing.List`
- `typing.Optional`
- `zipfile`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/forensics/archive_intelligence.improvements.md

# Improvements for archive_intelligence

**File**: `src\\logic\agents\forensics\archive_intelligence.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 74 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `archive_intelligence_test.py` with pytest tests

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

import tarfile
import zipfile


class ArchiveIntelligence:
    """Refactored logic from Archive Alchemist for safe archive analysis.
    Focuses on detecting malicious patterns like ZipSlip or massive compression ratios.
    """

    @staticmethod
    async def analyze_zip(file_path: str) -> dict:
        results = {"vulnerabilities": [], "files": []}
        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                for info in zip_ref.infolist():
                    # Detect ZipSlip
                    if ".." in info.filename or info.filename.startswith("/"):
                        results["vulnerabilities"].append(
                            {
                                "type": "ZipSlip",
                                "file": info.filename,
                                "severity": "High",
                            }
                        )

                    # Detect massive expansion ratio (ZipBomb)
                    if info.file_size > 0:
                        ratio = info.compress_size / info.file_size
                        if ratio < 0.001 and info.file_size > 1024 * 1024:
                            results["vulnerabilities"].append(
                                {
                                    "type": "PotentialZipBomb",
                                    "file": info.filename,
                                    "ratio": ratio,
                                    "severity": "Medium",
                                }
                            )

                    results["files"].append(info.filename)
        except Exception as e:
            results["error"] = str(e)
        return results

    @staticmethod
    async def analyze_tar(file_path: str) -> dict:
        results = {"vulnerabilities": [], "files": []}
        try:
            with tarfile.open(file_path, "r:*") as tar_ref:
                for member in tar_ref.getmembers():
                    # Detect Directory Traversal (TarSlip)
                    if ".." in member.name or member.name.startswith("/"):
                        results["vulnerabilities"].append(
                            {"type": "TarSlip", "file": member.name, "severity": "High"}
                        )
                    results["files"].append(member.name)
        except Exception as e:
            results["error"] = str(e)
        return results
