# Pytest Failures and Warnings Report
Date: 2026-01-14

## Summary
- **Passed**: 840
- **Failed**: 158
- **Errors**: 257
- **Skipped**: 10
- **Warnings**: 13

## Major Failure Clusters

### 1. Infrastructure Tests (`tests/unit/infrastructure/`)
**Status**: Critical Systemic Failure (Import Error)
**Cause**: `load_agent_module` is failing to locate "backend/execution_engine.py".
**Affected Modules**:
- `test_backend_CORE_UNIT.py`
- `test_backend_LEGACY.py`
- `test_backend_UNIT.py`
- `test_gossip_UNIT.py` (Failures)
- `test_stats_SHELL.py` (Errors/Failures)

### 2. Core Tests (`tests/unit/core/`)
**Status**: Mixed Failures
**Cause**: Likely mismatched `BaseAgent` interface (V1 vs V2 attributes).
**Affected Modules**:
- `test_base_agent_CORE_UNIT.py`
- `test_base_agent_LEGACY.py`
- `test_base_agent_UNIT.py`
- `test_context_CORE_UNIT.py`
- `test_context_UNIT.py`

### 3. Utility Tests (`tests/unit/test_utils/`)
**Status**: Systemic Errors
**Cause**: Likely dependency on broken infrastructure fixtures or path resolution.
**Affected Modules**:
- `test_test_utils_COMPREHENSIVE_UNIT.py`
- `test_test_utils_CORE_UNIT.py`
- `test_test_utils_INTEGRATION.py`
- `test_test_utils_PERFORMANCE.py`
- `test_test_utils_UNIT.py`

### 4. Logic Tests (`tests/unit/logic/`)
**Status**: ✅ **PASSED** (Repaired in previous cycle)
- `test_agent_UNIT.py`
- `test_agent_ADVANCED_UNIT.py`
- `test_agent_LEGACY.py`

## Analyzed Root Causes
1. **Infrastructure Path Rot**: The file `backend/execution_engine.py` referenced in `tests/unit/infrastructure/conftest.py` likely no longer exists at that path or relative location.
2. **Missing Conftest Propagation**: The fixes applied to `tests/unit/logic/conftest.py` (Legacy Adapter) are not present in `tests/unit/core/conftest.py`, leading to `AttributeError` for `selective_agents`, `metrics`, etc. on BaseAgent.

## Remediation Plan
1. **Fix Infrastructure Fixture**: Locate `execution_engine.py` and update `tests/unit/infrastructure/conftest.py`.
2. **Standardize Legacy Adapter**: Extract `LegacyAgentWrapper` from `tests/unit/logic/conftest.py` and move it to a shared location (e.g., `tests/utils/legacy_adapter.py` or root `tests/conftest.py`) or duplicate it to `tests/unit/core/conftest.py`.

