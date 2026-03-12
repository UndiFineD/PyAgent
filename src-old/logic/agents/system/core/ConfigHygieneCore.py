"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/ConfigHygieneCore.description.md

# ConfigHygieneCore

**File**: `src\\logic\agents\\system\\core\\ConfigHygieneCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 51  
**Complexity**: 2 (simple)

## Overview

Core logic for Config Hygiene (Phase 174).
Handles JSON Schema validation for configuration files.

## Classes (1)

### `ConfigHygieneCore`

Class ConfigHygieneCore implementation.

**Methods** (2):
- `validate_json_with_schema(data_path, schema_path)`
- `extract_env_vars(config_data, prefix)`

## Dependencies

**Imports** (4):
- `json`
- `os`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/ConfigHygieneCore.improvements.md

# Improvements for ConfigHygieneCore

**File**: `src\\logic\agents\\system\\core\\ConfigHygieneCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 51 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: ConfigHygieneCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConfigHygieneCore_test.py` with pytest tests

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

"""
Core logic for Config Hygiene (Phase 174).
Handles JSON Schema validation for configuration files.
"""

import json
import os
from typing import Any


class ConfigHygieneCore:
    @staticmethod
    def validate_json_with_schema(data_path: str, schema_path: str) -> tuple[bool, str]:
        """Validates a JSON file against a schema.
        Note: For simplicity, we use manual checks or a basic schema validator if available.
        Since we want to avoid extra heavy dependencies like 'jsonschema' if not present,
        we'll do a structural check.
        """
        if not os.path.exists(data_path) or not os.path.exists(schema_path):
            return False, "File or schema missing."

        try:
            with open(data_path, encoding="utf-8") as f:
                data = json.load(f)
            with open(schema_path, encoding="utf-8") as f:
                schema = json.load(f)

            # Basic structural validation (check keys)
            if "required" in schema:
                for req in schema["required"]:
                    if req not in data:
                        return False, f"Missing required field: {req}"

            return True, "Validation successful."
        except Exception as e:
            return False, str(e)

    @staticmethod
    def extract_env_vars(
        config_data: dict[str, Any], prefix: str = "PYAGENT_"
    ) -> dict[str, str]:
        """Helper to flatten nested config into env-style key-value pairs.
        """
        env_vars = {}
        for k, v in config_data.items():
            if isinstance(v, (str, int, float, bool)):
                env_vars[f"{prefix}{k.upper()}"] = str(v)
            elif isinstance(v, dict):
                sub = ConfigHygieneCore.extract_env_vars(v, f"{prefix}{k.upper()}_")
                env_vars.update(sub)
        return env_vars
