# Description: `agent_test_utils.py`

## Module purpose

`src/agent_test_utils.py` contains reusable utilities for the repository’s agent
tests and development tooling. It includes structured dataclasses/enums,
generators and harness helpers, and a small set of legacy import utilities used
by older tests.

## Location

- Path: `src/agent_test_utils.py`

## Public surface

- Commonly used classes (representative, not exhaustive):
  - `MockAIBackend`
  - `FixtureGenerator`, `TestDataGenerator`
  - `FileSystemIsolator`, `PerformanceTracker`, `SnapshotManager`
  - `TestResultAggregator`, `AgentAssertions`
- Legacy helpers:
  - `agent_dir_on_path()`
  - `agent_sys_path()`
  - `load_module_from_path()`
  - `load_agent_module()`
  - `get_base_agent_module()`

## Behavior summary

- Provides test-support types and helpers; no CLI entrypoint.
- Some legacy helpers temporarily mutate `sys.path` to support older tests.
- `load_agent_module()` loads a module by file path and generates a safe module
  name when needed.

## Key dependencies

- Standard library heavy: `importlib.util`, `contextlib`, `dataclasses`,
  `pathlib`, `tempfile`, `shutil`, `threading`, `logging`, `json`, `re`, `sys`
- Optional: `numpy` (some utilities tolerate it being unavailable)

## File fingerprint

- SHA256(source): `7232856B2E51E2AB2E60A852AE65E26C13D0FEF42115EC7B011CB34BED287D93`
