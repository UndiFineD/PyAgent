# idea000002-missing-compose-dockerfile - Quality & Security Review

_Agent: @8ql | Date: 2026-03-31 | Branch: prj0000109-idea000002-missing-compose-dockerfile_
_Status: BLOCKED_

## Scope
| File | Change type |
|------|-------------|
| docs/project/kanban.json | Modified (pre-existing local drift, out-of-scope for this closure) |
| deploy/compose.yaml | Previously modified in project implementation scope (evidence reviewed) |
| deploy/docker-compose.yaml | Previously modified in project implementation scope (evidence reviewed) |
| deploy/Dockerfile.pyagent | Previously modified in project implementation scope (evidence reviewed) |
| deploy/Dockerfile.fleet | Added in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_dockerfile_paths.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_context_contract.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_dockerfile_regression_matrix.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_file_selection.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_non_goal_guardrails.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/deploy/test_compose_scope_boundary_markers.py | Previously modified in project implementation scope (evidence reviewed) |
| tests/docs/test_agent_workflow_policy_docs.py | Previously modified in project implementation scope (evidence reviewed) |
| docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md | Modified |

## Part A - Security Findings
| ID | Severity | File | Line | Rule | Description |
|----|----------|------|------|------|-------------|
| SEC-001 | MEDIUM | pip_audit_results.json / .github/agents/data/pip_audit_current_8ql.json | n/a | A06-Vulnerable Components | CVE delta vs committed baseline persists (requests:CVE-2026-25645, cryptography:CVE-2026-34073, pygments:CVE-2026-4539); classified as baseline quality debt outside active project implementation scope. |
| SEC-002 | INFO | tests/deploy/*.py; tests/docs/test_agent_workflow_policy_docs.py | multiple | S101 | Ruff `--select S` reports test-only assert usage; non-blocking in test scope. |

## Part B - Quality Gaps
| # | Type | Description | Responsible agent | Blocking? |
|---|------|-------------|-------------------|-----------|
| 1 | Governance | `python scripts/project_registry_governance.py validate` fails for this project: lane mismatch `json='Review'`, `kanban='Discovery'`. | @1project | YES |
| 2 | Scope constraint | User scope rule requires leaving pre-existing local modification in `docs/project/kanban.json` untouched, so blocker cannot be remediated in this closure pass. | @0master / @1project | YES |

## Part C - Lessons Written
| Pattern | Agent memory file | Recurrence | Promoted to agent rule? |
|---------|------------------|-----------|------------------------|
| Registry lane mismatch between project registry and kanban state blocks @8ql closure when unsynchronized. | .github/agents/data/current.8ql.memory.md | 5 | Already promoted (HARD) |

## OWASP Coverage
| Category | Status | Notes |
|----------|--------|-------|
| A01 Broken Access Control | PASS | No access-control changes in scope. |
| A02 Cryptographic Failures | PASS | No new crypto handling introduced in scope. |
| A03 Injection | PASS | No new command/SQL interpolation observed in scoped assets. |
| A04 Insecure Design | PASS | Non-goal guardrails and deterministic contract tests are present. |
| A05 Security Misconfiguration | PASS | No workflow permission/config changes in this closure scope. |
| A06 Vulnerable Components | FINDING (MEDIUM) | Baseline CVE delta persists; tracked as unresolved quality debt. |
| A07 Identification and Authentication Failures | PASS | No auth-path changes in scope. |
| A08 Software and Data Integrity Failures | PASS | No untrusted artifact execution change detected in scope. |
| A09 Security Logging and Monitoring Failures | PASS | Existing logging/validation evidence captured. |
| A10 SSRF | PASS | No network fetch path changes in scope. |

## Checks Run (Evidence)
1. `git branch --show-current` -> PASS (`prj0000109-idea000002-missing-compose-dockerfile`)
2. `git diff --name-only HEAD` -> `docs/project/kanban.json`
3. `git ls-files --others --exclude-standard` -> PASS (none)
4. `git diff --name-only HEAD -- .github/workflows/*.yml` -> PASS (no workflow changes)
5. `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_context_contract.py tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py` -> PASS (19 passed)
6. `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> PASS (15 passed)
7. `.venv\Scripts\ruff.exe check --select S --output-format concise -- tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_context_contract.py tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py tests/docs/test_agent_workflow_policy_docs.py` -> INFO (S101 test-only findings)
8. `.venv\Scripts\ruff.exe format --check tests/deploy/test_compose_scope_boundary_markers.py tests/docs/test_agent_workflow_policy_docs.py` -> PASS (`2 files already formatted`)
9. `python scripts/project_registry_governance.py validate` -> FAIL (`Lane mismatch for prj0000109: json='Review', kanban='Discovery'`)
10. `pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json` + delta parser -> MEDIUM (3 new findings vs committed baseline)

## Verdict
| Gate | Status |
|------|--------|
| Security (CodeQL / ruff-S / CVEs / workflow) | PASS with MEDIUM debt (non-blocking) |
| Plan vs delivery | PASS |
| AC vs test coverage | PASS |
| Docs vs implementation | PASS |
| Governance lane consistency | FAIL |
| **Overall** | **BLOCKED -> @1project** |
