# idea000014-processing - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-30_

## Implementation Summary
Resolved the @7exec deterministic no-op blocker with a minimal script-only normalization fix.

Changes keep generator/parity output stable by preserving already-committed package token casing from `requirements.txt` when matching dependencies case-insensitively.

This removes casing churn on no-op regeneration for repository expectations (`pyjwt`, `sqlalchemy`) while keeping existing test contracts intact.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| scripts/deps/generate_requirements.py | preserve existing requirements package-token casing during generation | +86/-1 |
| scripts/deps/check_dependency_parity.py | apply identical casing normalization before expected-content comparison | +89/-1 |
| requirements.txt | restore canonical committed casing for `pyjwt` and `sqlalchemy` lines | +2/-2 |

## Implementation Evidence (AC Mapping)
| AC ID | Changed module/file | Validating tests | Status |
|---|---|---|---|
| AC-002 | scripts/deps/generate_requirements.py | tests/deps/test_generate_requirements_deterministic.py | PASS |
| AC-003 | scripts/deps/check_dependency_parity.py | tests/deps/test_dependency_parity_gate.py | PASS |
| AC-004 | scripts/deps/check_dependency_parity.py | tests/deps/test_dependency_parity_gate.py::test_parity_failure_includes_remediation_command | PASS |
| AC-006 | scripts/deps/generate_requirements.py; scripts/deps/check_dependency_parity.py; requirements.txt | tests/deps/test_generate_requirements_deterministic.py; tests/deps/test_dependency_parity_gate.py; no-op generation/parity sequence | PASS |

## Test Run Results
```
Lint/docstring checks on changed scripts:
- ruff check --fix scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
  -> passed
- ruff check scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
  -> passed
- ruff check --select D scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
  -> passed

Deps tests:
- python -m pytest -q tests/deps
  -> 10 passed
- python -m pytest -q tests/deps/test_generate_requirements_deterministic.py tests/deps/test_dependency_parity_gate.py
  -> 6 passed

Exact blocker sequence:
- python scripts/deps/generate_requirements.py --output requirements.txt
- python scripts/deps/check_dependency_parity.py --check
- git diff --exit-code -- requirements.txt
  -> parity check passed; git diff exit 0 (no output)

No-placeholder scan on changed source files:
- rg --type py "raise NotImplementedError|raise NotImplemented\\b|#\\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" scripts/deps
- rg --type py "^\\s*\\.\\.\\.\\s*$" scripts/deps
  -> no matches
```

## Blocker Remediation Evidence (2026-03-30)
- Blocker: pre-commit E501 in tests/structure/test_kanban.py line 154.
- Fix: wrapped the single long assert line without behavior changes.
- Validation: `pre-commit run --files tests/structure/test_kanban.py` -> passed.

## Deferred Items
none

## Handoff
Target agent: @7exec
Runtime validation readiness: READY
