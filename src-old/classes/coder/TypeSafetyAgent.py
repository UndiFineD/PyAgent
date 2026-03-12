#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/TypeSafetyAgent.description.md

# TypeSafetyAgent

**File**: `src\classes\coder\TypeSafetyAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in Python type hint enforcement and 'Any' type elimination.

## Classes (1)

### `TypeSafetyAgent`

**Inherits from**: BaseAgent

Identifies missing type annotations and 'Any' usage to improve codebase robustness.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze_file(self, target_path)`
- `run_audit(self, directory)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `ast`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/TypeSafetyAgent.improvements.md

# Improvements for TypeSafetyAgent

**File**: `src\classes\coder\TypeSafetyAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 102 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TypeSafetyAgent_test.py` with pytest tests

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

"""Agent specializing in Python type hint enforcement and 'Any' type elimination."""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function


class TypeSafetyAgent(BaseAgent):
    """Identifies missing type annotations and 'Any' usage to improve codebase robustness."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Type Safety Agent. "
            "Your role is to enforce strict type hinting across the codebase. "
            "Scan for: Function parameters without types, missing return types, and 'Any' type usage. "
            "Provide specific suggestions to replace 'Any' with more descriptive types."
        )

    def _get_default_content(self) -> str:
        return "# Type Safety Audit\n\n## Summary\nWaiting for analysis...\n"

    def analyze_file(self, target_path: Path) -> List[Dict[str, Any]]:
        """Analyzes a single Python file for type safety issues."""
        issues = []
        try:
            content = target_path.read_text(encoding="utf-8")
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check arguments
                    for arg in node.args.args:
                        if arg.annotation is None and arg.arg != "self":
                            issues.append(
                                {
                                    "line": node.lineno,
                                    "type": "Missing Param Type",
                                    "item": f"Parameter '{arg.arg}' in '{node.name}'",
                                    "severity": "MEDIUM",
                                }
                            )

                    # Check return type
                    if node.returns is None:
                        issues.append(
                            {
                                "line": node.lineno,
                                "type": "Missing Return Type",
                                "item": f"Function '{node.name}'",
                                "severity": "LOW",
                            }
                        )

                # Check for 'Any'
                elif isinstance(node, ast.Name) and node.id == "Any":
                    issues.append(
                        {
                            "line": node.lineno,
                            "type": "Usage of 'Any'",
                            "item": "Variable or annotation using 'Any'",
                            "severity": "HIGH",
                        }
                    )

        except Exception as e:
            logging.error(f"Failed to analyze {target_path}: {e}")

        return issues

    def run_audit(self, directory: str = "src") -> str:
        """Runs a full type safety audit on the directory."""
        root = Path(directory)
        all_issues = []

        for py_file in root.rglob("*.py"):
            if any(p in str(py_file) for p in ["__pycache__", "venv", ".git"]):
                continue

            file_issues = self.analyze_file(py_file)
            if file_issues:
                all_issues.append((py_file.name, file_issues))

        if not all_issues:
            return "✅ No type safety issues detected in the analyzed scope."

        report = ["## Type Safety Analysis Report\n"]
        for filename, issues in all_issues:
            report.append(f"### {filename}")
            for issue in issues:
                icon = "🚨" if issue["severity"] == "HIGH" else "⚠️"
                report.append(
                    f"- {icon} **{issue['type']}**: {issue['item']} (Line {issue['line']})"
                )

        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Perform a type safety audit."""
        path = prompt if prompt else "src/classes"
        return self.run_audit(path)


if __name__ == "__main__":
    main = create_main_function(
        TypeSafetyAgent, "TypeSafety Agent", "Path to audit (e.g. 'src/classes')"
    )
    main()
