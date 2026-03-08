#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/ConfigAgent.description.md

# ConfigAgent

**File**: `src\classes\specialized\ConfigAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 62  
**Complexity**: 4 (simple)

## Overview

Agent specializing in configuration validation, secrets checking, and environment setup.
Inspired by external-secrets and infrastructure-as-code patterns.

## Classes (1)

### `ConfigAgent`

**Inherits from**: BaseAgent

Ensures the agent fleet has all necessary configurations and API keys.

**Methods** (4):
- `__init__(self, file_path)`
- `validate_env(self)`
- `validate_models_yaml(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `yaml`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/ConfigAgent.improvements.md

# Improvements for ConfigAgent

**File**: `src\classes\specialized\ConfigAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConfigAgent_test.py` with pytest tests

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

"""Agent specializing in configuration validation, secrets checking, and environment setup.
Inspired by external-secrets and infrastructure-as-code patterns.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class ConfigAgent(BaseAgent):
    """Ensures the agent fleet has all necessary configurations and API keys."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Config Agent. "
            "Your role is to verify the environment and project settings. "
            "Check for missing API keys, invalid YAML configs, and environment contradictions. "
            "Never display secret values in your output."
        )

    @as_tool
    def validate_env(self) -> str:
        """Checks for required environment variables."""
        required = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "WORKSPACE_ROOT"]
        missing = [key for key in required if key not in os.environ]

        report = ["## ⚙️ Environment Validation\n"]
        if not missing:
            report.append("✅ All required environment variables are set.")
        else:
            report.append(f"❌ **Missing variables**: {', '.join(missing)}")

        return "\n".join(report)

    @as_tool
    def validate_models_yaml(self) -> str:
        """Verifies the integrity of models.yaml."""
        config_path = self.workspace_root / "config" / "models.yaml"
        if not config_path.exists():
            return "❌ `config/models.yaml` not found."

        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)

            # Simple structure check
            if "models" in data and isinstance(data["models"], list):
                return (
                    f"✅ `models.yaml` is valid. Detected {len(data['models'])} models."
                )
            else:
                return "❌ `models.yaml` has invalid structure (missing 'models' list)."
        except Exception as e:
            return f"❌ Error parsing `models.yaml`: {e}"

    def improve_content(self, prompt: str) -> str:
        return self.validate_env()
