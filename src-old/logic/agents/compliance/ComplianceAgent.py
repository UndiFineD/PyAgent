"""LLM_CONTEXT_START

## Source: src-old/logic/agents/compliance/ComplianceAgent.description.md

# ComplianceAgent

**File**: `src\\logic\agents\\compliance\\ComplianceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 57  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ComplianceAgent.

## Classes (1)

### `ComplianceAgent`

**Inherits from**: BaseAgent

Shell agent for continuous compliance and regulatory auditing.
Coordinates fleet-wide scans and reports violations to the security layer.

**Methods** (2):
- `__init__(self, file_path)`
- `perform_audit(self, file_map)`

## Dependencies

**Imports** (6):
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `src.logic.agents.compliance.core.ComplianceCore.ComplianceCore`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/compliance/ComplianceAgent.improvements.md

# Improvements for ComplianceAgent

**File**: `src\\logic\agents\\compliance\\ComplianceAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 57 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ComplianceAgent_test.py` with pytest tests

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

import logging
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool
from src.core.base.Version import VERSION

# Ensure relative or absolute import matches structure
try:
    from src.logic.agents.compliance.core.ComplianceCore import (
        ComplianceCore,
    )
except ImportError:
    # If core doesn't exist yet, we might need to mock or it is in a different place
    pass

__version__ = VERSION


class ComplianceAgent(BaseAgent):
    """Shell agent for continuous compliance and regulatory auditing.
    Coordinates fleet-wide scans and reports violations to the security layer.
    """

    def __init__(self, file_path: str | None = None) -> None:
        super().__init__(file_path if file_path else "virtual_compliance_agent")
        try:
            self.core = ComplianceCore()
        except NameError:
            self.core = None  # Handle missing core gracefully
        self.history: list[dict[str, Any]] = []

    @as_tool
    def perform_audit(self, file_map: dict[str, str]) -> dict[str, Any]:
        """Audits a map of file_paths to content."""
        if not self.core:
            return {"status": "ERROR", "message": "ComplianceCore missing"}

        all_issues = []
        for path, content in file_map.items():
            issues = self.core.audit_content(content, path)
            all_issues.extend(issues)

        score = self.core.aggregate_score(all_issues)

        report = {
            "score": score,
            "issue_count": len(all_issues),
            "critical_violations": [
                i.message for i in all_issues if i.severity == "CRITICAL"
            ],
            "status": "PASS" if score > 0.8 else "FAIL",
        }

        self.history.append(report)
        logging.info(f"Compliance Report: Score {score:.2f} ({report['status']})")

        return report
