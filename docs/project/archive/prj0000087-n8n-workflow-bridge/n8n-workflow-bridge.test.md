# n8n-workflow-bridge - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-27_

## Test Plan
Write red-phase contract tests for n8n bridge v1 based on plan AC-01..AC-06.

Approach:
1. Create aggregate red target test module with all 18 contract tests.
2. Create per-module test files for structure and focused module contracts.
3. Ensure failures are assertion-driven red failures (not import-time crashes).
4. Run red target and structure checks, then record results and handoff for implementation.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| RT-01..RT-18 | n8n bridge v1 contract tests (config, adapter, client, core, mixin, contract path) | tests/test_n8n_bridge.py | RED (20 failed as expected) |
| SM-01 | Module-focused config contract checks | tests/test_N8nBridgeConfig.py | AUTHORED |
| SM-02 | Module-focused adapter contract checks | tests/test_N8nEventAdapter.py | AUTHORED |
| SM-03 | Module-focused HTTP client contract checks | tests/test_N8nHttpClient.py | AUTHORED |
| SM-04 | Module-focused core contract checks | tests/test_N8nBridgeCore.py | AUTHORED |
| SM-05 | Module-focused mixin delegation checks | tests/test_N8nBridgeMixin.py | AUTHORED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| RED-TARGET | FAILED (expected red) | `python -m pytest -q tests/test_n8n_bridge.py --tb=short` -> 20 failed in 1.35s |
| STRUCTURE | FAILED | `python -m pytest -q tests/structure --tb=short` -> 1 failed, 128 passed (tests/structure/test_kanban.py row-count assertion) |

## Unresolved Failures
1. Expected red failure in `tests/test_n8n_bridge.py` because `src.core.n8nbridge` does not exist yet.
2. Existing unrelated structure failure in `tests/structure/test_kanban.py::test_kanban_total_rows` expecting 88 rows, found 91.

