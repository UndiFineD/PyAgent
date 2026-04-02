# dev-tools-autonomy — Test

_Status: COMPLETE_
_Tester: @5test | Updated: 2026-03-22_

## Test Strategy
Unit test each tool module in isolation using `tmp_path` for filesystem
interactions. Mock subprocess calls where needed to avoid network/env dependency.

## Test Cases

| ID | Test | File | Status |
|----|------|------|--------|
| T1 | `check_dependencies` returns a list | tests/tools/test_dependency_audit.py | PASS |
| T2 | `analyze_file` returns dict with expected keys | tests/tools/test_metrics.py | PASS |
| T3 | `analyze_directory` returns list for a known dir | tests/tools/test_metrics.py | PASS |
| T4 | `run_heal` returns list of actions | tests/tools/test_self_heal.py | PASS |
| T5 | `load_plugin` raises ValueError for unlisted name | tests/tools/test_plugin_loader.py | PASS |
| T6 | `load_plugin` succeeds for allowlisted name | tests/tools/test_plugin_loader.py | PASS |
| T7 | Modules importable without side effects | tests/tools/test_dependency_audit.py | PASS |

## Edge Cases Covered
- Empty directory passed to `analyze_directory`.
- Empty `allowed` list in `load_plugin`.
- Self-heal idempotency (running twice produces same result).
