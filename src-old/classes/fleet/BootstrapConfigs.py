#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/BootstrapConfigs.description.md

# BootstrapConfigs

**File**: `src\classes\fleet\BootstrapConfigs.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 0 imports  
**Lines**: 73  
**Complexity**: 0 (simple)

## Overview

Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/BootstrapConfigs.improvements.md

# Improvements for BootstrapConfigs

**File**: `src\classes\fleet\BootstrapConfigs.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 73 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BootstrapConfigs_test.py` with pytest tests

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
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""

BOOTSTRAP_AGENTS = {
    # System Agents that might not follow standard naming or search patterns
    "Orchestrator": (
        "src.classes.specialized.StructuredOrchestrator",
        "StructuredOrchestrator",
        None,
    ),
    "Sandbox": ("src.classes.coder.SandboxAgent", "SandboxAgent", None),
    "Linguist": ("src.classes.specialized.LinguisticAgent", "LinguisticAgent", None),
    "Audit": ("src.classes.specialized.EternalAuditAgent", "EternalAuditAgent", None),
}

BOOTSTRAP_ORCHESTRATORS = {
    "self_healing": (
        "src.classes.orchestration.SelfHealingOrchestrator",
        "SelfHealingOrchestrator",
    ),
    "telemetry": ("src.classes.stats.ObservabilityEngine", "ObservabilityEngine"),
    "self_improvement": (
        "src.classes.orchestration.SelfImprovementOrchestrator",
        "SelfImprovementOrchestrator",
    ),
    "registry": ("src.classes.orchestration.ToolRegistry", "ToolRegistry"),
    "signals": ("src.classes.orchestration.SignalRegistry", "SignalRegistry"),
    "recorder": ("src.classes.backend.LocalContextRecorder", "LocalContextRecorder"),
    "sql_metadata": ("src.classes.backend.SqlAgent", "SqlAgent"),
    "global_context": (
        "src.classes.context.GlobalContextEngine",
        "GlobalContextEngine",
    ),
    "fallback_engine": ("src.classes.stats.ModelFallbackEngine", "ModelFallbackEngine"),
    "core": ("src.classes.fleet.FleetCore", "FleetCore"),
}
