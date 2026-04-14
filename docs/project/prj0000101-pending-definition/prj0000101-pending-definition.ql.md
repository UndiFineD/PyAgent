# prj0000101-pending-definition - Security Scan Results

_Status: DONE_
_Scanner: @8ql | Updated: 2026-03-29_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| backend/app.py | Lint/security-style gate | ruff |
| tests/backend/test_health_probes_contract.py | Lint/security-style gate | ruff |
| tests/backend/test_health_probes_access_control.py | Lint/security-style gate | ruff |
| tests/backend/test_health_probes_security.py | Lint/security-style gate | ruff |
| backend/app.py | Type-check gate | mypy |

## Branch Gate
- Expected branch from project artifact: `prj0000101-pending-definition`
- Observed branch (`git branch --show-current`): `prj0000101-pending-definition`
- Result: PASS

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| QL-101-001 | LOW | backend/app.py | multiple | Initial ruff findings: import order blocks, one long line, local import placement. Remediated in-scope and rechecked PASS. |

## Applied In-Scope Remediation
- Reordered and normalized imports in `backend/app.py`.
- Hoisted local websocket imports to module scope to satisfy import-order rules.
- Wrapped one overlength SWOT default string to meet line-length policy.
- Preserved existing behavior; only lint-compliance adjustments were made.

## Verification Evidence
1. `python -m ruff check backend/app.py tests/backend/test_health_probes_contract.py tests/backend/test_health_probes_access_control.py tests/backend/test_health_probes_security.py` -> PASS after minimal fixes.
2. `python -m mypy --config-file mypy.ini backend/app.py` -> PASS.

## False Positives
| ID | Reason |
|---|---|
| None | n/a |

## Cleared
Current status: DONE
Gate decision: CLEAR for the health-probe slice checks requested in this pass.

## Residual Risks
- This @8ql pass was scoped to the requested files/commands only; full-repo security/dependency/workflow scans were not executed in this step.
