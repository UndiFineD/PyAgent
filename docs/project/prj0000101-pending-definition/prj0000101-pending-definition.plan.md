# prj0000101-pending-definition - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-29_

## Overview
Deliver a contract-complete health probe slice for @5test and @6code based on
design interfaces IFC-HC-101/102/103 and AC-101..AC-108. Scope covers backend
probe contract behavior, probe-focused test coverage, docs synchronization for
canonical probe usage, and pre-handoff validation/security evidence.

## Phased Task List

### Phase 1 - Backend Contract Implementation (@6code)
- [ ] T-401 - Implement canonical and alias health probes in FastAPI app.
	Objective: Implement `/v1/health` + `/health` and `/v1/livez` + `/livez`
	with contract-stable payloads and 200 status behavior.
	Target files: `backend/app.py`
	Acceptance criteria: AC-101, AC-102, AC-103
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_contract.py -k "health or livez"`

- [ ] T-402 - Implement readiness degradation contract and response safety.
	Objective: Implement `/v1/readyz` + `/readyz` with 200 ready path and 503
	degraded path driven by `app.state.readyz_degraded_reason` or
	`PYAGENT_READYZ_FORCE_DEGRADED`, including required `reason` field policy.
	Target files: `backend/app.py`
	Acceptance criteria: AC-101, AC-104, AC-105, AC-108
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_contract.py -k "readyz"`

- [ ] T-403 - Enforce probe unauthenticated and rate-limit exempt behavior.
	Objective: Ensure probe routes bypass auth/rate-limit behavior so probes do
	not return 401/403/429.
	Target files: `backend/app.py`, `backend/auth.py`, `backend/rate_limiter.py`
	Acceptance criteria: AC-106, AC-107
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_access_control.py`

### Phase 2 - Probe Test Suite (@5test)
- [ ] T-451 - Add canonical-vs-alias parity and status-code tests.
	Objective: Add probe contract tests for health/liveness/readiness parity,
	status codes (200/503), and deterministic readiness transitions.
	Target files: `tests/backend/test_health_probes_contract.py`
	Acceptance criteria: AC-101, AC-102, AC-103, AC-104, AC-105
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_contract.py`

- [ ] T-452 - Add schema and payload safety tests for readiness degradation.
	Objective: Assert required keys and negative-field guardrails for degraded
	readiness payloads.
	Target files: `tests/backend/test_health_probes_security.py`
	Acceptance criteria: AC-105, AC-108
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_security.py`

- [ ] T-453 - Add auth/rate-limit probe behavior tests.
	Objective: Validate probe endpoints remain unauthenticated and rate-limit
	exempt under auth-enabled runtime and burst traffic simulation.
	Target files: `tests/backend/test_health_probes_access_control.py`
	Acceptance criteria: AC-106, AC-107
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_access_control.py`

### Phase 3 - Documentation Sync
- [ ] T-481 - Sync probe endpoint docs to canonical + alias path policy.
	Objective: Document probe endpoint paths, expected responses, and readiness
	degraded semantics for operators and integrators.
	Target files: `README.md`, `docs/setup.md`
	Acceptance criteria: Probe docs include `/v1/health`, `/v1/livez`,
	`/v1/readyz` and alias compatibility note; response examples are contract
	consistent with IFC-HC-101/102/103.
	Validation command:
	`python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

### Phase 4 - Validation + Security Gates Before Git Handoff
- [ ] T-491 - Execute focused runtime validation suite (@7exec).
	Objective: Produce pass/fail evidence for probe behavior, contract parity,
	and docs governance checks before @8ql/@9git.
	Target files: `backend/app.py`, `tests/backend/test_health_probes_contract.py`,
	`tests/backend/test_health_probes_access_control.py`,
	`tests/backend/test_health_probes_security.py`
	Acceptance criteria: All phase-2 probe tests pass; docs policy test passes.
	Validation command:
	`python -m pytest -q tests/backend/test_health_probes_contract.py tests/backend/test_health_probes_access_control.py tests/backend/test_health_probes_security.py tests/docs/test_agent_workflow_policy_docs.py`

- [ ] T-492 - Execute lint/type/security quality checks (@8ql pre-handoff).
	Objective: Verify no probe-related lint/type regressions and ensure
	readiness payload safety checks are green before @9git.
	Target files: `backend/app.py`, `tests/backend/test_health_probes_contract.py`,
	`tests/backend/test_health_probes_access_control.py`,
	`tests/backend/test_health_probes_security.py`
	Acceptance criteria: Ruff and mypy checks pass for touched probe scope;
	security-oriented probe tests pass with no disallowed payload fields.
	Validation command:
	`python -m ruff check backend/app.py tests/backend/test_health_probes_contract.py tests/backend/test_health_probes_access_control.py tests/backend/test_health_probes_security.py`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Backend probe contract implementation | T-401, T-402, T-403 | NOT_STARTED |
| M2 | Probe test suite complete | T-451, T-452, T-453 | NOT_STARTED |
| M3 | Documentation synchronized | T-481 | NOT_STARTED |
| M4 | Validation and security gates complete | T-491, T-492 | NOT_STARTED |
| M5 | Ready for @9git handoff | M1-M4 complete | NOT_STARTED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# @7exec focused validation
python -m pytest -q tests/backend/test_health_probes_contract.py
python -m pytest -q tests/backend/test_health_probes_access_control.py
python -m pytest -q tests/backend/test_health_probes_security.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# @8ql pre-handoff quality/security checks
python -m ruff check backend/app.py tests/backend/test_health_probes_contract.py tests/backend/test_health_probes_access_control.py tests/backend/test_health_probes_security.py
python -m mypy --config-file mypy.ini backend/app.py
```
