#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/SecurityAgent.description.md

# SecurityAgent

**File**: `src\classes\coder\SecurityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 27  
**Complexity**: 2 (simple)

## Overview

Agent specializing in Security Auditing and Vulnerability detection.

## Classes (1)

### `SecurityAgent`

**Inherits from**: BaseAgent

Agent for security analysis of code and configuration.

**Methods** (2):
- `__init__(self, file_path)`
- `_get_default_content(self)`

## Dependencies

**Imports** (3):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/SecurityAgent.improvements.md

# Improvements for SecurityAgent

**File**: `src\classes\coder\SecurityAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 27 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityAgent_test.py` with pytest tests

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

"""Agent specializing in Security Auditing and Vulnerability detection."""


from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function


class SecurityAgent(BaseAgent):
    """Agent for security analysis of code and configuration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Senior Security Auditor. "
            "Scan the provided content for vulnerabilities, hardcoded secrets, "
            "SQL injection risks, cross-site scripting (XSS), and insecure dependencies. "
            "Provide detailed remediation steps for each finding."
        )

    def _get_default_content(self) -> str:
        return "# Security Audit Report\n\n## Summary\nPending audit...\n"


if __name__ == "__main__":
    main = create_main_function(
        SecurityAgent, "Security Agent", "File to audit for security"
    )
    main()
