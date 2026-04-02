# private-key-remediation - Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-28_

## Branch Gate
- Expected branch: `prj0000090-private-key-remediation`
- Observed branch: `prj0000090-private-key-remediation`
- Result: PASS

## Policy Compliance
- Code of conduct (`docs/project/code_of_conduct.md`): PASS
- Naming standards (`docs/project/naming_standards.md`): PASS

## Test Plan
Scope: Chunk 001 test-first tasks from plan (`T1`, `T3`, `T5`, `T7`) only.

Approach:
- Add failing behavior tests for scanner contracts, rotation gate transitions, CI/pre-commit guardrails, and containment cleanup.
- Ensure red failures are meaningful contract/assertion failures (not collection-time import crashes).
- Keep changes limited to test files and project artifacts; no production code changes in this phase.

Validation commands executed (red phase):
- `python -m pytest -q tests/security/test_secret_scan_service_contract.py tests/security/test_scan_report_schema.py`
- `python -m pytest -q tests/security/test_rotation_checkpoint_service.py tests/security/test_rotation_gate_decision.py`
- `python -m pytest -q tests/security/test_secret_guardrail_policy.py tests/security/test_ci_secret_guardrail_job.py tests/security/test_pre_commit_secret_hook.py`
- `python -m pytest -q tests/security/test_containment_cleanup.py tests/security/test_private_key_artifact_absence.py`
- `ruff check --fix <new test files>`
- `ruff check <new test files>`
- `ruff check --select D <new test files>`

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-T1-001 | SecretScanService exposes profile methods `scan_tree`, `scan_refs`, `scan_history` | tests/security/test_secret_scan_service_contract.py | RED |
| TC-T1-002 | Secret scan finding keys are deterministic after normalization | tests/security/test_secret_scan_service_contract.py | RED |
| TC-T1-003 | Scanner execution failure is fail-closed with `ERROR` + blocking outcome | tests/security/test_secret_scan_service_contract.py | RED |
| TC-T1-004 | ScanReport requires `run_id` and status enum `PASS/FAIL/ERROR` | tests/security/test_scan_report_schema.py | RED |
| TC-T1-005 | ScanReport blocking semantics enforce HIGH/CRITICAL gate | tests/security/test_scan_report_schema.py | RED |
| TC-T3-001 | `begin_incident` records incident id and compromised fingerprint | tests/security/test_rotation_checkpoint_service.py | RED |
| TC-T3-002 | `record_rotation_step` requires non-empty `evidence_uri` | tests/security/test_rotation_checkpoint_service.py | RED |
| TC-T3-003 | `evaluate_gate` transitions `BLOCKED -> PARTIAL -> COMPLETE` deterministically | tests/security/test_rotation_gate_decision.py | RED |
| TC-T5-001 | Guardrail policy blocks PR on HIGH/CRITICAL findings | tests/security/test_secret_guardrail_policy.py | RED |
| TC-T5-002 | Guardrail policy blocks push on CRITICAL findings | tests/security/test_secret_guardrail_policy.py | RED |
| TC-T5-003 | Security CI workflow defines dedicated secret scan job | tests/security/test_ci_secret_guardrail_job.py | RED |
| TC-T5-004 | Security CI workflow includes fail-closed behavior for secret findings | tests/security/test_ci_secret_guardrail_job.py | RED |
| TC-T5-005 | Pre-commit config contains secret-scan hook | tests/security/test_pre_commit_secret_hook.py | RED |
| TC-T5-006 | Pre-commit hook invokes secret scanner before commit | tests/security/test_pre_commit_secret_hook.py | RED |
| TC-T5-007 | Pre-commit and CI share same tree-profile invocation contract | tests/security/test_pre_commit_secret_hook.py | RED |
| TC-T7-001 | Remediation runbook includes containment evidence + incident linkage | tests/security/test_containment_cleanup.py | RED |
| TC-T7-002 | Cleanup verifier script exists and enforces repo-scoped checks | tests/security/test_containment_cleanup.py | RED |
| TC-T7-003 | Active tree excludes leaked private-key artifact path | tests/security/test_private_key_artifact_absence.py | RED |

## AC-to-Test Matrix
| AC ID | Covered Test Case IDs |
|---|---|
| AC-001 | TC-T1-001, TC-T1-003, TC-T7-003 |
| AC-002 | TC-T3-001, TC-T3-002, TC-T3-003 |
| AC-003 | TC-T5-001, TC-T5-002, TC-T5-003, TC-T5-004, TC-T5-005, TC-T5-006, TC-T5-007 |
| AC-004 | TC-T1-001, TC-T1-002, TC-T1-004, TC-T3-001, TC-T3-003 |
| AC-005 | TC-T7-001, TC-T7-002, TC-T7-003 |
| AC-006 | TC-T1-001, TC-T1-002, TC-T1-003, TC-T1-005, TC-T5-001, TC-T5-002, TC-T5-003, TC-T5-004, TC-T5-005, TC-T5-006, TC-T5-007 |

## Weak-Test Detection Gate
- Gate result: PASS (no weak tests detected)
- Checks performed:
	- No placeholder tests (`assert True`, TODO-only tests, or existence-only import checks).
	- Contract tests assert concrete behavior and state transitions.
	- Red-phase failures are assertion/contract failures with explicit messages; no collection-time `ImportError`/`AttributeError` abort.

## Validation Results
| ID | Result | Output |
|---|---|---|
| CMD-T1 | FAIL (expected RED) | `5 failed in 4.86s` - missing `src.security.secret_scan_service` / `src.security.models.scan_report` contract modules via assertion-style failures |
| CMD-T3 | FAIL (expected RED) | `3 failed in 4.32s` - missing `src.security.rotation_checkpoint_service` contract module via assertion-style failures |
| CMD-T5 | FAIL (expected RED) | `7 failed in 2.15s` - missing `src.security.secret_guardrail_policy` plus CI/pre-commit guardrail assertions failing against current configs |
| CMD-T7 | FAIL (expected RED) | `3 failed in 1.49s` - missing runbook and verifier script; leaked key artifact path still present |
| CMD-LINT | PASS | `ruff check --fix` auto-fixed style; `ruff check` and `ruff check --select D` both pass |

## Unresolved Failures
- Missing implementation modules under `src/security/**` for scanner contracts, rotation checkpoint service, and guardrail policy.
- Missing remediation artifacts: `docs/security/private-key-remediation-runbook.md` and `scripts/security/verify_no_key_material.py`.
- `rust_core/2026-03-11-keys.priv` still exists, violating active-tree containment target.

## Handoff To @6code
- Handoff status: READY
- Required implementation scope (Chunk 001):
	- `src/security/secret_scan_service.py`
	- `src/security/models/scan_report.py`
	- `src/security/rotation_checkpoint_service.py`
	- `src/security/secret_guardrail_policy.py`
	- `.github/workflows/security.yml` (add secret-scan fail-closed gate)
	- `.pre-commit-config.yaml` (add secret-scan local hook)
	- `docs/security/private-key-remediation-runbook.md`
	- `scripts/security/verify_no_key_material.py`
	- containment result for `rust_core/2026-03-11-keys.priv`
