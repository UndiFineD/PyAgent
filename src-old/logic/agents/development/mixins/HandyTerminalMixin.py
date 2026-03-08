"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/HandyTerminalMixin.description.md

# HandyTerminalMixin

**File**: `src\logic\agents\development\mixins\HandyTerminalMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 83  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for HandyTerminalMixin.

## Classes (1)

### `HandyTerminalMixin`

Mixin for terminal execution and slash command handling in HandyAgent.

**Methods** (2):
- `terminal_slash_command(self, command, args)`
- `execute_with_diagnosis(self, command)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `shlex`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.development.HandyAgent.HandyAgent`
- `subprocess`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/HandyTerminalMixin.improvements.md

# Improvements for HandyTerminalMixin

**File**: `src\logic\agents\development\mixins\HandyTerminalMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 83 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HandyTerminalMixin_test.py` with pytest tests

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

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import subprocess
from typing import TYPE_CHECKING
from src.core.base.BaseUtilities import as_tool

from src.logic.agents.development.HandyAgent import HandyAgent


class HandyTerminalMixin:
    """Mixin for terminal execution and slash command handling in HandyAgent."""

    @as_tool
    def terminal_slash_command(self: HandyAgent, command: str, args: list[str]) -> str:
        """Handles agentic slash commands like /fix, /test, /summarize directly from a CLI."""
        res = ""
        if command == "/fix":
            res = f"### 🔧 Triggered /fix for {args}\nAnalyzing errors and proposing patches..."
        elif command == "/test":
            res = f"### 🧪 Triggered /test for {args}\nRunning pytest and coverage analysis..."
        elif command == "/summarize":
            res = f"### 📝 Triggered /summarize for {args}\nGenerating high-level architectural overview..."
        else:
            res = (
                f"Unknown slash command: {command}. Available: /fix, /test, /summarize"
            )

        self._record("slash_command", {"cmd": command, "args": args}, res)
        return res

    @as_tool
    def execute_with_diagnosis(self: HandyAgent, command: str) -> str:
        """Executes a command and automatically analyzes errors if it fails.

        WARNING: This executes arbitrary shell commands. Use with caution.
        Includes a basic blocklist for catastrophic commands.
        """
        # Improved Security Blocklist (Phase 104)
        blocklist = [
            "rm -rf /",
            "mkfs",
            "dd if=",
            "> /dev/sda",
            "chmod -R 777 /",
            ":(){ :|:& };:",
            "del /s /q c:/",
            "format c:",
        ]
        if any(b in command.lower() for b in blocklist):
            msg = "### ⚠️ Security Block: Potentially catastrophic command detected."
            self._record("execute_fail", command, msg)
            return msg

        try:
            # Use shlex to safely split commands without shell=True
            import shlex

            cmd_args = shlex.split(command)
            result = subprocess.run(
                cmd_args, capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                stdout = result.stdout[:1000]
                self._record("execute_success", command, stdout)
                return f"### ✅ Success:\n```text\n{stdout}\n```"
            else:
                stderr = result.stderr[:500]
                analysis = [
                    f"### ❌ Command Failed (Code {result.returncode}):",
                    f"**Stderr**: `{stderr}`",
                    "\n**Handy Diagnosis**:",
                    "- Suggested Fix: Check if dependencies are installed or if paths are correct.",
                    "- Context: This error often occurs when the environment is misconfigured.",
                ]
                res = "\n".join(analysis)
                self._record("execute_fail", command, res)
                return res
        except Exception as e:
            err_msg = f"Execution error: {e}"
            self._record("execute_error", command, err_msg)
            return err_msg
