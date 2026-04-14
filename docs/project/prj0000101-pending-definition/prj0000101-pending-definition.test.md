# prj0000101-pending-definition - Test Artifacts

_Status: IN_PROGRESS_
_Tester: @5test | Updated: 2026-03-29_

## Test Plan
Objective: Define a failing-first, contract-driven probe test strategy for
IFC-HC-101, IFC-HC-102, and IFC-HC-103 so @6code can implement endpoint
behavior with deterministic pass/fail signals.

Design contract tie-in:
- IFC-HC-101 (`/v1/health`, `/health`): 200 with `{\"status\":\"ok\"}` parity.
- IFC-HC-102 (`/v1/livez`, `/livez`): 200 with `{\"status\":\"alive\"}` parity.
- IFC-HC-103 (`/v1/readyz`, `/readyz`): 200 ready path and 503 degraded path
	with required degraded keys and safe reason payload.

Test categories and coverage:
1. Unit tests (probe logic + schema helper)
	 - Validate readiness decision helper behavior for env/state degradation
		 signals and normalization of truthy values.
	 - Validate response schema helper for canonical JSON contracts and required
		 degraded fields.
2. API/integration tests (endpoint + status semantics)
	 - Validate endpoint status semantics for health/livez/readyz on canonical
		 and alias paths.
	 - Validate deterministic 200 vs 503 behavior on readiness based on local
		 state and env overrides.
3. Regression tests (alias parity + non-breaking behavior)
	 - Validate canonical vs alias parity for status code and response payload
		 shape/value.
	 - Validate legacy aliases remain supported and behavior-compatible.
4. Security/policy checks
	 - Validate probe endpoints remain unauthenticated under auth-enabled
		 runtime (no 401/403).
	 - Validate probe endpoints remain limiter-exempt under burst traffic (no
		 429).
	 - Validate degraded readiness payload excludes sensitive/internal fields
		 (no secrets, stack traces, tokens, filesystem paths, internals).

### AC-to-Test Matrix (Blocking)

| AC ID | Contract Requirement | Test Case IDs |
|---|---|---|
| AC-101 | Canonical + alias endpoints are available | TC-INT-001, TC-REG-001 |
| AC-102 | Health parity, 200, `{\"status\":\"ok\"}` | TC-INT-001, TC-REG-001 |
| AC-103 | Livez parity, 200, `{\"status\":\"alive\"}` | TC-INT-002, TC-REG-002 |
| AC-104 | Readyz returns 200 + `{\"status\":\"ready\"}` when healthy | TC-UNIT-001, TC-INT-003 |
| AC-105 | Readyz returns 503 degraded payload with required fields | TC-UNIT-002, TC-INT-004, TC-SEC-002 |
| AC-106 | Probe endpoints unauthenticated | TC-SEC-001 |
| AC-107 | Probe endpoints rate-limit exempt | TC-SEC-003 |
| AC-108 | No sensitive degraded payload leakage | TC-SEC-002 |

### Weak-Test Detection Gate (Blocking)

Reject and revise any test that:
- passes against placeholder implementations (`pass`, `return None`, stubbed
	constants),
- only asserts import/existence/non-None/isinstance without behavior checks,
- only asserts no exception,
- uses unconditional assertions (`assert True`) or TODO placeholders.

Gate check method:
- Red phase must fail due to contract assertion mismatch (wrong status/payload),
	not due to import or missing symbol errors.
- Green phase must include at least one semantic assertion per test on status
	code and payload keys/values.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-UNIT-001 | Readiness decision helper returns ready (200 semantics) when no degraded signal is set | tests/backend/test_health_probe_logic_unit.py | RED_PLANNED |
| TC-UNIT-002 | Readiness response schema helper enforces degraded fields (`status`, `ready=false`, `reason`) and rejects invalid forms | tests/backend/test_health_probe_logic_unit.py | RED_PLANNED |
| TC-INT-001 | `/v1/health` and `/health` return 200 and identical payload/schema `{\"status\":\"ok\"}` | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-INT-002 | `/v1/livez` and `/livez` return 200 and identical payload/schema `{\"status\":\"alive\"}` | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-INT-003 | `/v1/readyz` and `/readyz` return 200 + `{\"status\":\"ready\"}` when healthy | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-INT-004 | `/v1/readyz` and `/readyz` return 503 + degraded payload contract when forced degraded | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-REG-001 | Health canonical/alias parity remains non-breaking for legacy callers | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-REG-002 | Livez canonical/alias parity remains non-breaking for legacy callers | tests/backend/test_health_probes_contract.py | RED_PLANNED |
| TC-SEC-001 | Probe endpoints do not require auth and never return 401/403 under auth-enabled runtime | tests/backend/test_health_probes_access_control.py | RED_PLANNED |
| TC-SEC-002 | Degraded readiness payload blocks sensitive fields and unsafe reason strings | tests/backend/test_health_probes_security.py | RED_PLANNED |
| TC-SEC-003 | Probe endpoints are rate-limit exempt and do not return 429 under burst traffic | tests/backend/test_health_probes_access_control.py | RED_PLANNED |

## Failing-First Intent for @6code Handoff
- Before implementation, red-phase probe tests should fail on semantic contract
	assertions, such as:
	- expected 503 degraded readiness but received 200,
	- missing required degraded fields (`ready`, `reason`),
	- canonical/alias payload mismatch,
	- unexpected auth/rate-limit status for probes.
- Failures that are import/symbol-not-found are non-actionable for contract
	verification and require test hardening before handoff.

Expected red selectors (before @6code implementation is complete):
- `python -m pytest -q tests/backend/test_health_probes_contract.py`
- `python -m pytest -q tests/backend/test_health_probes_access_control.py`
- `python -m pytest -q tests/backend/test_health_probes_security.py`

## Validation Results
| ID | Result | Output |
|---|---|---|
| DOC-POLICY-001 | PASS | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |

## Command Set

Environment activation:
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
```

Red/green probe test execution:
```powershell
python -m pytest -q tests/backend/test_health_probe_logic_unit.py
python -m pytest -q tests/backend/test_health_probes_contract.py
python -m pytest -q tests/backend/test_health_probes_access_control.py
python -m pytest -q tests/backend/test_health_probes_security.py
```

Project policy docs validation:
```powershell
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

## Unresolved Failures
None at artifact-definition stage. Red-phase behavioral failures are expected
once test files are authored and executed against pre-implementation behavior.
