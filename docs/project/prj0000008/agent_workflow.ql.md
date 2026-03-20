# agent_workflow - Security Scan Results

_Status: DONE_
_Scanner: @8ql | Updated: 2026-03-20_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| `src/core/workflow/task.py` | ruff S | ruff |
| `src/core/workflow/queue.py` | ruff S | ruff |
| `src/core/workflow/engine.py` | ruff S | ruff |
| `src/cort/__init__.py` | ruff S | ruff |

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| F-01 | LOW | `src/core/workflow/queue.py` | 33 | S101: assert in validate() — internal contract guard |
| F-02 | LOW | `src/core/workflow/engine.py` | 27 | S101: assert in validate() — internal contract guard |

## False Positives
| ID | Reason |
|---|---|
| F-01, F-02 | Both asserts are inside `validate()` functions used by quality-gate tests only. Not reachable from untrusted input. |

## Cleared
- **CRITICAL findings**: 0
- **HIGH findings**: 0
- **MEDIUM findings**: 0
- **LOW/INFO findings**: 2 (both false positives)
- **pip-audit new CVEs**: 0
- **Decision**: CLEAR — no blocker for @9git
