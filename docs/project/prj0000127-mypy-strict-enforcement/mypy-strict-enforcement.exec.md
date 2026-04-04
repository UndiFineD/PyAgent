# mypy-strict-enforcement - Execution Log

_Status: IN_PROGRESS_
_Executor: @7exec | Updated: 2026-04-04_
## Execution Plan
Warn-phase execution only for T-MYPY-004..T-MYPY-006.

## Warn-Phase Runbook (T-MYPY-006)
### Rollback taxonomy
- F1: Config authority mismatch (strict lane does not explicitly use `--config-file pyproject.toml`).
- F2: Deterministic strict-lane regression inside the phase-1 allowlist.
- F3: CI instability/flapping that makes strict-lane outcomes non-deterministic.

### Warn -> required promotion prerequisites
- The strict lane remains warn-only until promotion evidence is complete.
- Promotion threshold marker: N=5 consecutive green strict-lane executions in warn mode.
- The broad lane remains warn-only throughout this project.
- Promotion is out of scope for this slice; this runbook documents prerequisites only.

### Required -> warning rollback policy
- If F1 is detected, immediately keep or return strict lane to warning mode and restore explicit config authority.
- If F3 is detected after promotion, downgrade required -> warning and preserve diagnostics.
- Re-promotion requires a fresh N=5 consecutive-green sequence in warn mode.

## Run Log
`
TBD
`

## Pass/Fail Summary
| Check | Status | Notes |
|---|---|---|
| pytest -q | | |
| mypy | | |
| ruff | | |

## Blockers
none

