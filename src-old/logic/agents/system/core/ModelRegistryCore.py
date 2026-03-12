"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/ModelRegistryCore.description.md

# ModelRegistryCore

**File**: `src\logic\agents\system\core\ModelRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 68  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for ModelRegistryCore.

## Classes (1)

### `ModelRegistryCore`

ModelRegistryCore manages the PEFT (LoRA/QLoRA) adapter registry.
It maps request types to specific expert adapters.
Phase 289: Model Registry Self-Healing.

**Methods** (6):
- `__init__(self)`
- `self_heal(self)`
- `get_adapter_for_task(self, task_type)`
- `should_trigger_finetuning(self, quality_history, threshold)`
- `register_new_adapter(self, name, path)`
- `list_adapters(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/ModelRegistryCore.improvements.md

# Improvements for ModelRegistryCore

**File**: `src\logic\agents\system\core\ModelRegistryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ModelRegistryCore_test.py` with pytest tests

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

from typing import Dict, List, Optional
from pathlib import Path
import logging


class ModelRegistryCore:
    """
    ModelRegistryCore manages the PEFT (LoRA/QLoRA) adapter registry.
    It maps request types to specific expert adapters.
    Phase 289: Model Registry Self-Healing.
    """

    def __init__(self) -> None:
        # Registry mapping intent/type to adapter path
        self.adapter_registry: dict[str, str] = {
            "python_expert": "models/forge/adapters/python_312_lora",
            "security_audit": "models/forge/adapters/security_specialist_lora",
            "documentation": "models/forge/adapters/docgen_lora",
            "rust_developer": "models/forge/adapters/rust_migration_expert",
        }
        self.unhealthy_entries: set[str] = set()

    def self_heal(self) -> int:
        """
        Phase 289: Detects missing adapter files and prunes or fixes the registry.
        Returns the number of healed/removed entries.
        """
        healed_count = 0
        current_adapters = list(self.adapter_registry.items())

        for name, path_str in current_adapters:
            path = Path(path_str)
            if not path.exists():
                logging.warning(
                    f"ModelRegistry: Adapter '{name}' path '{path_str}' is missing. Healing..."
                )
                del self.adapter_registry[name]
                self.unhealthy_entries.add(name)
                healed_count += 1

        if healed_count > 0:
            logging.info(
                f"ModelRegistry: Self-healing complete. {healed_count} entries removed."
            )
        return healed_count

    def get_adapter_for_task(self, task_type: str) -> str | None:
        """Returns the adapter path for a given task type."""
        adapter = self.adapter_registry.get(task_type.lower())
        if adapter and not Path(adapter).exists():
            self.self_heal()
            return self.adapter_registry.get(task_type.lower())
        return adapter

    def should_trigger_finetuning(
        self, quality_history: list[float], threshold: float = 0.6
    ) -> bool:
        """
        Determines if fine-tuning is needed (e.g., last 5 scores below threshold).
        """
        if len(quality_history) < 5:
            return False

        last_5 = quality_history[-5:]
        return all(q < threshold for q in last_5)

    def register_new_adapter(self, name: str, path: str) -> None:
        """Adds a new adapter to the registry."""
        self.adapter_registry[name.lower()] = path

    def list_adapters(self) -> list[str]:
        """Lists all registered expert adapters."""
        return list(self.adapter_registry.keys())
