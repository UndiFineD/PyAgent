
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/core/BashCore.description.md

# BashCore

**File**: `src\\logic\agents\\development\\core\\BashCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 65  
**Complexity**: 2 (simple)

## Overview

Core logic for Bash script analysis (Phase 175).
Integrates shellcheck for linting generated scripts.

## Classes (1)

### `BashCore`

Class BashCore implementation.

**Methods** (2):
- `lint_script(script_path, recorder)`
- `wrap_with_safety_flags(content)`

## Dependencies

**Imports** (4):
- `json`
- `os`
- `src.core.base.interfaces.ContextRecorderInterface`
- `subprocess`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/core/BashCore.improvements.md

# Improvements for BashCore

**File**: `src\\logic\agents\\development\\core\\BashCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 65 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: BashCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BashCore_test.py` with pytest tests

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

"""
Core logic for Bash script analysis (Phase 175).
Integrates shellcheck for linting generated scripts.
"""

import os
import subprocess

from src.core.base.interfaces import ContextRecorderInterface


class BashCore:
    @staticmethod
    def lint_script(script_path: str, recorder: ContextRecorderInterface | None = None) -> dict:
        """Runs shellcheck on a bash script.
        """
        if not os.path.exists(script_path):
            result = {"error": "File not found"}
            if recorder:
                recorder.record_interaction("bash", "shellcheck", script_path, "file-not-found")
            return result

        try:
            # -f json for machine readable output
            result = subprocess.run(["shellcheck", "-f", "json", script_path], capture_output=True, text=True)
            if result.stdout:
                import json
                findings = {"issues": json.loads(result.stdout), "valid": False}
            else:
                findings = {"issues": [], "valid": True}

            if recorder:
                recorder.record_interaction(
                    provider="bash",
                    model="shellcheck",
                    prompt=script_path,
                    result=str(findings)[:2000]
                )

            return findings
        except FileNotFoundError:
            result = {"error": "shellcheck not found. Please install it to enable bash linting."}
        except Exception as e:
            result = {"error": str(e)}

        if recorder:
            recorder.record_interaction(
                provider="bash",
                model="shellcheck",
                prompt=script_path,
                result=str(result)[:2000]
            )
        return result

    @staticmethod
    def wrap_with_safety_flags(content: str) -> str:
        """Ensures script starts with common safety flags if not present.
        """
        header = "#!/bin/bash\nset -euo pipefail\n\n"
        if content.startswith("#!"):
            # If shebang exists but no flags, we could inject. For now, just a helper.
            return content
        return header + content
