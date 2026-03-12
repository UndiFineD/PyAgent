#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/AgentRegistryCore.description.md

# AgentRegistryCore

**File**: `src\\classes\fleet\\AgentRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.

## Classes (1)

### `AgentRegistryCore`

Pure logic core for Agent Registry.

**Methods** (5):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`
- `validate_agent_structure(self, agent_instance, required_methods)`

## Dependencies

**Imports** (7):
- `VersionGate.VersionGate`
- `os`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/AgentRegistryCore.improvements.md

# Improvements for AgentRegistryCore

**File**: `src\\classes\fleet\\AgentRegistryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentRegistryCore_test.py` with pytest tests

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
AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

from .VersionGate import VersionGate


class AgentRegistryCore:
    """Pure logic core for Agent Registry."""

    def __init__(self, current_sdk_version: str) -> None:
        self.sdk_version: str = current_sdk_version

    def process_discovered_files(
        self, file_paths: List[str]
    ) -> Dict[str, Tuple[str, str, Optional[str]]]:
        """Processes a list of file paths and extracts agent/orchestrator configurations.
        Expects relative paths from workspace root.
        """
        discovered: Dict[str, Tuple[str, str, Optional[str]]] = {}

        for rel_path in file_paths:
            file = os.path.basename(rel_path)
            if (
                file.endswith("Agent.py") or file.endswith("Orchestrator.py")
            ) and not file.startswith("__"):
                agent_name: str = file[:-3]
                module_path: str = (
                    rel_path.replace(os.path.sep, ".")
                    .replace("/", ".")
                    .replace(".py", "")
                )

                # Phase 105: Discovered agents should not default to their own file path as arg
                discovered[agent_name] = (module_path, agent_name, None)

                # Add short name (e.g. "Coder" for "CoderAgent")
                if agent_name.endswith("Agent"):
                    short_name: str = agent_name[:-5]
                    if short_name and short_name not in discovered:
                        discovered[short_name] = (module_path, agent_name, None)
                elif agent_name.endswith("Orchestrator"):
                    short_name: str = agent_name[:-12]
                    if short_name and short_name not in discovered:
                        discovered[short_name] = (module_path, agent_name, None)
        return discovered

    def parse_manifest(
        self, raw_manifest: Dict[str, Any]
    ) -> Dict[str, Tuple[str, str, Optional[str]]]:
        """Parses the raw manifest dictionary and filters incompatible plugins.
        Returns a dict of {AgentName: (module, class, config)}.
        """
        valid_configs: Dict[str, Tuple[str, str, Optional[str]]] = {}
        for key, cfg in raw_manifest.items():
            # Expecting: "AgentName": ["module.path", "ClassName", "arg_path", "min_sdk_version"]
            if isinstance(cfg, list) and len(cfg) >= 2:
                # Extract potential version gate
                min_sdk: str = cfg[3] if len(cfg) > 3 else "1.0.0"

                if self.is_compatible(min_sdk):
                    config_path: Optional[str] = cfg[2] if len(cfg) > 2 else None
                    valid_configs[key] = (cfg[0], cfg[1], config_path)

        return valid_configs

    def is_compatible(self, required_version: str) -> bool:
        """Gatekeeper check using centralized logic.
        """
        return VersionGate.is_compatible(self.sdk_version, required_version)

    def validate_agent_structure(
        self, agent_instance: Any, required_methods: List[str] = None
    ) -> List[str]:
        """Checks if an agent instance has the required methods.
        Returns a list of missing methods.
        """
        missing = []
        reqs = required_methods or ["execute", "describe"]
        for method in reqs:
            if not hasattr(agent_instance, method):
                missing.append(method)
        return missing
