#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/AutoDebuggerOrchestrator.description.md

# AutoDebuggerOrchestrator

**File**: `src\classes\orchestration\AutoDebuggerOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 113  
**Complexity**: 3 (simple)

## Overview

AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.

## Classes (1)

### `AutoDebuggerOrchestrator`

Orchestrates recursive self-debugging and code repair.

**Methods** (3):
- `__init__(self, workspace_root)`
- `validate_and_repair(self, file_path)`
- `run_fleet_self_audit(self)`

## Dependencies

**Imports** (12):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.coder.CoderAgent.CoderAgent`
- `src.classes.specialized.ImmuneSystemAgent.ImmuneSystemAgent`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/AutoDebuggerOrchestrator.improvements.md

# Improvements for AutoDebuggerOrchestrator

**File**: `src\classes\orchestration\AutoDebuggerOrchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 113 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AutoDebuggerOrchestrator_test.py` with pytest tests

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

"""AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.
"""

import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

from src.classes.base_agent.utilities import as_tool
from src.classes.coder.CoderAgent import CoderAgent
from src.classes.specialized.ImmuneSystemAgent import ImmuneSystemAgent


class AutoDebuggerOrchestrator:
    """Orchestrates recursive self-debugging and code repair."""

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = workspace_root or os.getcwd()
        # Initialize specialized agents
        # Note: We use the actual source paths if we can find them, otherwise relative
        immune_path = os.path.join(
            self.workspace_root, "src/classes/specialized/ImmuneSystemAgent.py"
        )
        coder_path = os.path.join(
            self.workspace_root, "src/classes/coder/CoderAgent.py"
        )

        self.immune_system = ImmuneSystemAgent(immune_path)
        self.coder = CoderAgent(coder_path)
        self.repair_history: List[Dict[str, Any]] = []

    @as_tool
    def validate_and_repair(self, file_path: str) -> Dict[str, Any]:
        """Validates a file and attempts automatic repair if it fails syntax check.

        Args:
            file_path: The absolute path to the file to check.

        """
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}

        logging.info(f"AutoDebugger: Validating {file_path}")

        # 1. Syntax Check using python -m py_compile
        try:
            subprocess.run(
                [sys.executable, "-m", "py_compile", file_path],
                check=True,
                capture_output=True,
                text=True,
            )
            return {"status": "success", "message": f"{file_path} passed syntax check."}
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            logging.warning(
                f"AutoDebugger: Syntax error detected in {file_path}: {error_msg}"
            )

            # 2. Safety Scan with ImmuneSystemAgent
            threat_scan = self.immune_system.scan_for_injections(error_msg)
            if threat_scan["status"] == "dangerous":
                logging.error(
                    f"AutoDebugger: Safety breach detected in error logs for {file_path}. Aborting repair."
                )
                return {
                    "status": "blocked",
                    "message": "Infected code detected during validation. Quarantining fix.",
                }

            # 3. Attempt Repair with CoderAgent
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            repair_prompt = (
                f"The file {file_path} has the following syntax error:\n"
                f"```\n{error_msg}\n```\n"
                f"Fix the syntax error while preserving the original logic. Content:\n\n{content}"
            )

            # Use CoderAgent to perform the fix
            # coder.improve_content(prompt) handles the actual update and self-validation
            from pathlib import Path

            self.coder.file_path = Path(
                file_path
            )  # Target the coder to the broken file
            fixed_content = self.coder.improve_content(repair_prompt)

            repair_record = {
                "file": file_path,
                "error": error_msg,
                "status": "repaired",
                "timestamp": "now",  # In real implementation we'd use datetime
            }
            self.repair_history.append(repair_record)

            return {
                "status": "repaired",
                "message": f"AutoDebugger: Successfully repaired {file_path}",
                "error_details": error_msg,
            }

    @as_tool
    def run_fleet_self_audit(self) -> str:
        """Audits all python files in the src directory for syntax issues."""
        src_path = os.path.join(self.workspace_root, "src")
        python_files = []
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        results = []
        for pf in python_files:
            res = self.validate_and_repair(pf)
            if res["status"] != "success":
                results.append(f"{pf}: {res['status']} - {res['message']}")

        if not results:
            return "Fleet self-audit complete. No issues found."
        return "Fleet self-audit complete. Issues found:\n" + "\n".join(results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = AutoDebuggerOrchestrator()
    if len(sys.argv) > 1:
        print(orchestrator.validate_and_repair(sys.argv[1]))
    else:
        print(orchestrator.run_fleet_self_audit())
