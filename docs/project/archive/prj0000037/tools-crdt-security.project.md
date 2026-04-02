# tools-crdt-security

**Project ID:** `prj0000037`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Create a central tool registry for `src/tools/` and add CLI dispatch support.
- [x] Implement usable versions of key tools (`git_utils`, `netcalc`, `nettest`, `ssl_utils`) rather than placeholders.
- [x] Ensure each tool supports `--help` and behaves as a real CLI utility.
- [x] Update `docs/tools.md` with usage examples and verify it covers all registered tools.
- [x] Add unit tests for tool registry and for each tool's core functionality.
- [x] Ensure `tests/tools/test_tools_sanity.py` remains green and exercises each tool’s main entrypoint.
- [x] Ensure all tools are async-friendly where required (no blocking loops).
- [x] Provide a `9git` alias tool for the `@9git` agent workflow (implements Git helper operations via `git_utils`).

## Status

8 of 8 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\inference\tools.rs`
  - `rust_core\src\security.rs`
  - `src\chat\mcp_tools.py`
  - `src\core\crdt_bridge.py`
  - `src\core\security_bridge.py`
  - `tests\backend\test_health_probes_security.py`
  - `tests\structure\test_dev_tools_dirs.py`
  - `tests\test_crdt_bridge.py`
  - `tests\test_crdt_error_mapping.py`
  - `tests\test_crdt_ffi_contract.py`
  - `tests\test_crdt_ffi_feature_flag.py`
  - `tests\test_crdt_ffi_observability.py`
  - `tests\test_crdt_ffi_parity.py`
  - `tests\test_crdt_ffi_performance.py`
  - `tests\test_crdt_ffi_validation.py`
  - `tests\test_crdt_merge_determinism.py`
  - `tests\test_crdt_payload_codec.py`
  - `tests\test_rust_crdt_merge.py`
  - `tests\test_security_bridge.py`
  - `tests\test_security_rotation.py`
  - `tests\test_tools_sanity.py`
  - `tests\tools\test_tools_cli.py`
  - `tests\tools\test_tools_docs.py`
  - `tests\tools\test_tools_registry.py`