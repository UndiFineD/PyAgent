# 8ql Memory

This file tracks security scan results, CodeQL findings, 
and dependency audit outcomes.

## Auto-handoff

Once security scans and CodeQL analysis are complete, 
the next agent in the workflow is **@9git**. 
Invoke it via `agent/runSubagent` to continue the process.

## Last scan - 2026-03-29 (prj0000099)
- Task: prj0000099-stub-module-elimination
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000099-stub-module-elimination
- Branch gate: PASS (expected = observed = `prj0000099-stub-module-elimination`)
- Files scanned: `docs/project/prj0000099-stub-module-elimination/*`, branch delta governance/project files (`.github/agents/data/*project-memory`, `data/projects.json`, `data/nextproject.md`, `docs/project/kanban.md`, `docs/project/ideas/idea000011-stub-module-elimination.md`)
- Security - CodeQL: SKIPPED (lightweight scoped gate per request)
- Security - ruff S rules: PASS (project-scope package entrypoint check clean; repo-level run shows 12 pre-existing out-of-scope findings)
- Security - pip-audit new findings: 0 (`Deps with vulns: 0` from committed `pip_audit_results.json`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` unchanged in project scope)
- Security - Workflow injection: PASS (no changed `.github/workflows/*.yml` files)
- Quality - Plan vs delivery: PASS (validation-first closure artifacts present and aligned)
- Quality - AC vs test coverage: PASS (`PASS` API evidence check + focused pytest `5 passed in 1.69s`)
- Quality - Docs vs implementation: PASS (required project artifacts present, ql artifact finalized)
- Quality - Agent file consistency: PASS
- Lessons written: 0 (no new recurring pattern)
- Rules promoted: 0
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Last scan - 2026-03-29 (prj0000098 rerun after blocker fixes)
- Task: prj0000098-backend-health-check-endpoint
- Lifecycle: IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000098-backend-health-check-endpoint
- Branch gate: PASS (expected = observed = `prj0000098-backend-health-check-endpoint`)
- Files scanned: project-scoped backend probe/test/docs files plus branch delta support files listed in `prj0000098-backend-health-check-endpoint.ql.md`
- Security - CodeQL: SKIPPED (no project-scoped CodeQL DB invocation in this rerun)
- Security - ruff S rules: PASS WITH NOTES (12 pre-existing repo findings; no project-scoped HIGH/CRITICAL)
- Security - pip-audit new findings: 0 (`Deps with vulns: 0` from committed baseline parse)
- Security - Rust unsafe check: SKIPPED (`rust_core/` unchanged)
- Security - Workflow injection: PASS (no changed `.github/workflows/*.yml` files)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (policy blocker test and readiness degraded-path tests pass)
- Quality - Docs vs implementation: PASS WITH NON-BLOCKING NOTE (design wording drift only)
- Quality - Agent file consistency: PASS
- Lessons written: 1 (rerun evidence capture pattern)
- Rules promoted: 0
- Outcome: CLEAN -> @9git
- handoff_target: @9git

### Lesson - 2026-03-29 (prj0000098 rerun)
- Pattern: Blocker-remediation reruns are safest when they include direct single-test proof for the exact failing policy test before full handoff.
- Root cause: Prior blocker confidence relied on downstream notes before direct rerun in @8ql.
- Prevention: Always execute and record the exact previously failing test selector in the @8ql rerun evidence block.
- First seen: 2026-03-29
- Seen in: prj0000098-backend-health-check-endpoint
- Recurrence count: 1
- Promotion status: CANDIDATE

## Last scan - 2026-03-29 (prj0000098)
- Task: prj0000098-backend-health-check-endpoint
- Lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- status: BLOCKED
- task_id: prj0000098-backend-health-check-endpoint
- Branch gate: PASS (expected = observed = `prj0000098-backend-health-check-endpoint`)
- Files scanned: `backend/app.py`, `backend/rate_limiter.py`, `tests/test_api_versioning.py`, `tests/test_backend_auth.py`, `tests/test_rate_limiting.py`, `docs/project/prj0000098-backend-health-check-endpoint/*`, and branch-modified supporting docs/modules from current working tree
- Security - CodeQL: SKIPPED (no project-scoped CodeQL database invocation in this gate run)
- Security - ruff S rules: PASS WITH LOW (`backend/app.py` S311 on simulated metrics path; no HIGH/CRITICAL findings)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` reports `Deps with vulns: 0`; `pip-audit` CLI available)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified in this project scope)
- Security - Workflow injection: PASS (no changed `.github/workflows/*.yml` in current branch delta)
- Quality - Plan vs delivery: FAIL (scope/control drift and unresolved project git-summary policy block)
- Quality - AC vs test coverage: FAIL (design AC-004 readiness-degraded path not implemented/tested)
- Quality - Docs vs implementation: FAIL (`prj0000098-backend-health-check-endpoint.git.md` missing required `## Branch Plan` section)
- Quality - Agent file consistency: FAIL (project git-summary artifact does not meet current workflow policy format)
- Lessons written: 2 (`8ql.memory.md`)
- Rules promoted: 0
- Outcome: BLOCKED -> @6code (with @4plan/@5test alignment)
- handoff_target: @6code

### Lesson - 2026-03-29 (prj0000098)
- Pattern: New project `*.git.md` artifacts can be created without modern Branch Plan sections, causing policy-gate failures in execution and quality stages.
- Root cause: Downstream artifact updates did not migrate the git summary template to the required modern branch-plan format.
- Prevention: Before @7exec and @8ql handoff, enforce a docs-policy lint checkpoint for `docs/project/<project>/*.git.md` requiring `## Branch Plan` or explicit legacy exception.
- First seen: 2026-03-29
- Seen in: prj0000098-backend-health-check-endpoint
- Recurrence count: 1
- Promotion status: CANDIDATE

### Lesson - 2026-03-29 (prj0000098)
- Pattern: Design acceptance tables can diverge from plan/test/code artifacts when contract-level requirements are added in design but not propagated.
- Root cause: AC updates in design (`/readyz` degraded 503 path) were not reflected in plan tasks, tests, or implementation evidence.
- Prevention: Require an AC sync pass at @4plan closeout that diffs design AC rows against plan/test/code artifacts before handoff to @5test.
- First seen: 2026-03-29
- Seen in: prj0000098-backend-health-check-endpoint
- Recurrence count: 1
- Promotion status: CANDIDATE

## Last scan - 2026-03-29 (prj0000097)
- Task: prj0000097-stub-module-elimination
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000097-stub-module-elimination
- Branch gate: PASS (expected = observed = `prj0000097-stub-module-elimination`)
- Files scanned: `src/rl/__init__.py`, `src/speculation/__init__.py`, `tests/rl/*`, `tests/speculation/*`, `tests/guards/test_rl_speculation_import_scope.py`, `tests/test_rl_package.py`, `tests/test_speculation_package.py`, and project artifacts under `docs/project/prj0000097-stub-module-elimination/`
- Security - CodeQL: SKIPPED (no project-scoped CodeQL CLI/database run in this gate; ruff S + workflow + dependency checks executed)
- Security - ruff S rules: PASS WITH INFO (project-scope S101 findings in pytest asserts only; non-blocking)
- Security - pip-audit new findings: 0 (baseline delta `NEW_IDS=0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified in this scope)
- Security - Workflow injection: PASS (no changed `.github/workflows/*.yml` files in project diff)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (`python -m pytest -v --maxfail=1 tests/rl tests/speculation tests/guards/test_rl_speculation_import_scope.py` -> `18 passed`)
- Quality - Docs vs implementation: PASS (all required project artifacts present) with non-blocking policy-drift note on stale scope boundary text in project.md
- Quality - Agent file consistency: PASS
- Lessons written: 1 (`8ql.memory.md`)
- Rules promoted: 0
- Outcome: CLEAN -> @9git
- handoff_target: @9git

### Lesson - 2026-03-29 (prj0000097)
- Pattern: Project initialization scope boundary text can drift from downstream implementation scope, creating governance ambiguity at handoff.
- Root cause: `project.md` retained @1project-only scope boundary while later phases correctly modified production and test files for planned slice delivery.
- Prevention: Update project artifact scope boundary once @3design/@4plan confirm final implementation/test surface, before @9git handoff checks.
- First seen: prj0000097
- Seen in: prj0000097-stub-module-elimination
- Recurrence count: 1
- Promotion status: CANDIDATE

## Unresolved Quality-Debt Ledger
- Debt ID: QD-prj0000098-001
- Status: DONE
- Owner: @6code (with @9git artifact ownership)
- Originating project: prj0000098-backend-health-check-endpoint
- Description: `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md` lacks required modern `## Branch Plan` section, blocking policy test and quality gate.
- Exit criteria: Met on 2026-03-29 rerun (`test_git_summaries_use_modern_branch_plan_format_or_carry_legacy_exception` passed).

- Debt ID: QD-prj0000098-002
- Status: DONE
- Owner: @4plan (contract alignment) with @5test/@6code implementation follow-through
- Originating project: prj0000098-backend-health-check-endpoint
- Description: Design AC-004 (`/readyz` 503 degraded contract) is not represented in current plan tasks, tests, or code behavior.
- Exit criteria: Met on 2026-03-29 rerun (readiness degraded-path tests passed for `/v1/readyz` and `/readyz`).

- Debt ID: QD-prj0000098-003
- Status: DONE
- Owner: @6code (or @0master if scope split/rebranch required)
- Originating project: prj0000098-backend-health-check-endpoint
- Description: Branch contains non-project-scope file edits beyond the design AC-007 boundary (backend health endpoint + health tests).
- Exit criteria: Met on 2026-03-29 rerun (governing artifacts updated to include canonical `/v1/...` alignment scope and validated at branch gate).

- Debt ID: QD-prj0000097-001
- Status: OPEN
- Owner: @1project (or @6code if delegated)
- Originating project: prj0000097-stub-module-elimination
- Description: Project artifact scope boundary text is stale relative to approved and delivered slice implementation/test paths.
- Exit criteria: Update `prj0000097-stub-module-elimination.project.md` scope boundary/handoff wording to match final scoped delivery, then confirm @9git staging rules remain deterministic.

## Last scan - 2026-03-29 (prj0000096)
- Task: prj0000096-coverage-minimum-enforcement
- Lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- status: BLOCKED
- task_id: prj0000096-coverage-minimum-enforcement
- Branch gate: PASS (expected = observed = `prj0000096-coverage-minimum-enforcement`)
- Files scanned: `.github/workflows/ci.yml`, `pyproject.toml`, `tests/structure/test_ci_yaml.py`, `tests/test_coverage_config.py`, `docs/project/prj0000096-coverage-minimum-enforcement/*`
- Security - CodeQL: SKIPPED (no CodeQL CLI/database execution in this scoped gate run)
- Security - ruff S rules: PASS WITH NOTES (12 pre-existing `src/**` findings outside project scope; no project-scoped regression)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` reports `Deps with vulns: 0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified in project scope)
- Security - Workflow injection: PASS (no `pull_request_target`; explicit `permissions`; no unsafe user-controlled interpolation in `run:`)
- Quality - Plan vs delivery: FAIL (threshold source-of-truth drift: workflow hardcodes `--cov-fail-under=40`)
- Quality - AC vs test coverage: PASS (targeted project test bundle green)
- Quality - Docs vs implementation: FAIL (`coverage-minimum-enforcement.code.md` claims single policy knob while workflow duplicates threshold)
- Quality - Agent file consistency: PASS
- Lessons written: 2 (`6code.memory.md`, `7exec.memory.md`)
- Rules promoted: 0
- Outcome: BLOCKED -> @6code / @7exec
- handoff_target: @6code

## Unresolved Quality-Debt Ledger
- Debt ID: QD-prj0000096-001
- Status: OPEN
- Owner: @6code
- Originating project: prj0000096-coverage-minimum-enforcement
- Description: Coverage threshold policy drift between `pyproject.toml` and `.github/workflows/ci.yml` (`--cov-fail-under=40` hardcoded).
- Exit criteria: Remove hardcoded threshold duplication and enforce config-driven threshold linkage; update code/test artifacts; rerun @7exec + @8ql gates.

- Debt ID: QD-prj0000096-002
- Status: OPEN
- Owner: @7exec (with @0master for tooling path)
- Originating project: prj0000096-coverage-minimum-enforcement
- Description: `tests/zzz/test_zzg_codeql_sarif_gate.py::test_all_sarif_files_are_fresh` remains red due to stale SARIF artifacts (>24h) even when run with `CODEQL_REBUILD=1`.
- Exit criteria: Establish reliable SARIF refresh path (or runner prerequisite), regenerate SARIF artifacts, and confirm freshness test green in fail-fast/full-suite validation.

## Last scan - 2026-03-28 (prj0000094 reassessment after blocker fix)
- Task: prj0000094-idea-003-mypy-strict-enforcement
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000094-idea-003-mypy-strict-enforcement
- Branch gate: PASS (expected = observed = `prj0000094-idea-003-mypy-strict-enforcement`)
- Files scanned: `src/transactions/*TransactionManager.py`, `mypy-strict-lane.ini`, strict-lane test files, and project artifacts under `docs/project/prj0000094-idea-003-mypy-strict-enforcement/`
- Security - CodeQL: SKIPPED (CLI/database flow not invoked in this scoped reassessment)
- Security - ruff S rules: PASS WITH INFO/LOW (pytest `S101`; static-command `S603` in smoke test only)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` baseline reports `Deps with vulns: 0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (no workflow-file changes in current diff)
- Quality - Plan vs delivery: PASS WITH NOTES (non-blocking artifact status/checklist sync drift)
- Quality - AC vs test coverage: PASS (`python -m mypy --config-file mypy-strict-lane.ini` green; transaction regression suite 48/48)
- Quality - Docs vs implementation: PASS WITH NOTES (test/plan metadata needs sync)
- Quality - Agent file consistency: PASS
- Lessons written: 0 (existing lesson retained as CANDIDATE)
- Rules promoted: 0
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Last scan - 2026-03-28 (prj0000094)
- Task: prj0000094-idea-003-mypy-strict-enforcement
- Lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- status: BLOCKED
- task_id: prj0000094-idea-003-mypy-strict-enforcement
- Branch gate: PASS (expected = observed = `prj0000094-idea-003-mypy-strict-enforcement`)
- Files scanned: `mypy-strict-lane.ini`, `tests/structure/test_mypy_strict_lane_config.py`, `tests/structure/test_ci_yaml.py`, `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`, `.github/workflows/ci.yml`, project artifacts under `docs/project/prj0000094-idea-003-mypy-strict-enforcement/`
- Security - CodeQL: SKIPPED (CLI/database flow not invoked; scoped checks executed)
- Security - ruff S rules: PASS WITH INFO/LOW (pytest `S101` patterns + one static-command `S603` in smoke test)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` baseline reports `Deps with vulns: 0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (`permissions` explicit, no `pull_request_target`, no unsafe user-controlled interpolation in `run:`)
- Quality - Plan vs delivery: PASS WITH NOTES (implementation delivered; plan/test status fields need sync)
- Quality - AC vs test coverage: CONDITIONAL (targeted strict-lane tests pass; strict-lane mypy promotion command fails)
- Quality - Docs vs implementation: PASS WITH NOTES (artifact status/checklist drift)
- Quality - Agent file consistency: PASS
- Lessons written: 1
- Rules promoted: 0
- Outcome: BLOCKED -> @6code
- handoff_target: @6code

### Lesson - 2026-03-28 (prj0000094)
- Pattern: Wave allowlist expansion can expose transitive strict-lane typing errors outside directly edited files.
- Root cause: Newly allowlisted core modules pull in `src/transactions/*` dependencies with pre-existing typing debt.
- Prevention: Before declaring wave completion, run strict-lane mypy as a pre-merge gate and either include dependency remediation in scope or predefine rollback candidate trimming.
- First seen: prj0000094
- Seen in: prj0000094-idea-003-mypy-strict-enforcement
- Recurrence count: 1
- Promotion status: CANDIDATE

## Last scan - 2026-03-28 (prj0000093 final quick pass)
- Task: prj0000093-projectmanager-ideas-autosync
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000093-projectmanager-ideas-autosync
- Branch gate: PASS (expected = observed = `prj0000093-projectmanager-ideas-autosync`)
- Files scanned: `backend/app.py`, `web/apps/ProjectManager.tsx`, `web/apps/ProjectManager.test.tsx`, `tests/test_api_ideas.py`, `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.ql.md`
- Security - CodeQL: SKIPPED (quick-pass scope; targeted security lint executed)
- Security - ruff S rules: PASS WITH LOW (2x S311 in `backend/app.py` lines 165/167; simulated FLM metrics path)
- Security - pip-audit new findings: 0 (no new advisories introduced in this scoped pass)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (no `.github/workflows/*.yml` changes in this scope)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (targeted backend/frontend suites green)
- Quality - Docs vs implementation: PASS WITH GAPS (non-blocking design/frontend sort default mismatch; design schema field drift)
- Quality - Agent file consistency: PASS
- Lessons written: 0 (no new recurring pattern beyond existing entries)
- Rules promoted: 0
- Unresolved quality debt: 1 OPEN (non-blocking docs alignment)
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Unresolved Quality-Debt Ledger
- Debt ID: QD-prj0000094-001
- Status: DONE
- Owner: @6code (implementation) with @4plan (scope/rollback decision)
- Originating project: prj0000094-idea-003-mypy-strict-enforcement
- Description: Strict-lane promotion blocker on `src/transactions/*` was remediated by typing-only fixes and reassessed clean.
- Exit criteria: met on 2026-03-28 (`python -m mypy --config-file mypy-strict-lane.ini` -> success; transaction regression suite green).

- Debt ID: QD-prj0000093-001
- Status: OPEN
- Owner: @6code (or @3design if contract documentation is updated instead)
- Originating project: prj0000093-projectmanager-ideas-autosync
- Description: Frontend ideas fetch defaults (`sort=rank&order=asc`) and current `IdeaModel` schema differ from IFC-03/IFC-01 text that still documents `sort=priority&order=desc` and `priority/impact/urgency` response fields.
- Exit criteria: align code and docs to one canonical contract (either update design artifact or adjust implementation), then rerun scoped @7exec + @8ql checks.

## Last scan - 2026-03-28 (prj0000093)
- Task: prj0000093-projectmanager-ideas-autosync
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000093-projectmanager-ideas-autosync
- Branch gate: PASS (expected = observed = `prj0000093-projectmanager-ideas-autosync`)
- Files scanned: `backend/app.py`, `tests/test_api_ideas.py`, `web/apps/ProjectManager.tsx`, `web/apps/ProjectManager.test.tsx`, `docs/project/prj0000093-projectmanager-ideas-autosync/*`
- Security - CodeQL: SKIPPED (CLI/database flow not invoked; scoped controls executed)
- Security - ruff S rules: PASS WITH LOW (1 LOW: S311 in `backend/app.py` lines 165/167; outside `/api/ideas` path)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` baseline reports `Deps with vulns: 0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (no `.github/workflows/*.yml` changes in scope)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS WITH GAPS (frontend AC coverage gaps for empty/filter behavior)
- Quality - Docs vs implementation: PASS WITH GAPS (`/api/ideas` query/sort contract drift versus design/plan)
- Quality - Agent file consistency: PASS
- Lessons written: 2 (`6code.memory.md`, `5test.memory.md`)
- Rules promoted: 0
- Unresolved quality debt: 1 OPEN (non-blocking)
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Unresolved Quality-Debt Ledger
- Debt ID: QD-prj0000093-001
- Status: OPEN
- Owner: @6code (with @5test for AC coverage closure)
- Originating project: prj0000093-projectmanager-ideas-autosync
- Description: Design/plan query contract (`implemented=exclude&implemented_mode=active_or_released&sort=priority&order=desc` + `q` support) is not fully represented in current `/api/ideas` implementation/frontend invocation and associated frontend test coverage.
- Exit criteria: align backend/frontend to documented contract (or update docs/contracts), add missing frontend AC tests, then rerun scoped @7exec validation and @8ql gate.

## Last scan - 2026-03-28 (prj0000092)
- Task: prj0000092-mypy-strict-enforcement
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000092-mypy-strict-enforcement
- Branch gate: PASS (expected = observed = `prj0000092-mypy-strict-enforcement`)
- Files scanned: `mypy-strict-lane.ini`, `.github/workflows/ci.yml`, `src/core/universal/UniversalAgentShell.py`, strict-lane tests and fixtures, and `docs/project/prj0000092-mypy-strict-enforcement/*`
- Security - CodeQL: SKIPPED (CLI/database flow not invoked; required scoped checks executed)
- Security - ruff S rules: PASS for project scope (repository-wide `src/` run reports pre-existing unrelated findings)
- Security - pip-audit new findings: 3 (1 MEDIUM, 2 LOW; tracked as non-blocking dependency debt)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (`.github/workflows/ci.yml` reviewed; explicit permissions; no user-controlled interpolation in `run:`; no `pull_request_target`)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (`pytest` strict-lane set `9 passed`; strict-lane mypy clean)
- Quality - Docs vs implementation: PASS (all 7 project artifacts present and aligned)
- Quality - Agent file consistency: PASS
- Lessons written: 0
- Rules promoted: 0
- Unresolved quality debt: 1 non-blocking item (dependency CVE refresh)
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Unresolved Quality-Debt Ledger
- Debt ID: QD-prj0000092-001
- Status: OPEN
- Owner: @0master (route to @6code dependency maintenance)
- Originating project: prj0000092-mypy-strict-enforcement
- Description: `pip-audit` reports vulnerable packages requiring upgrades: `cryptography==46.0.5` -> `46.0.6`, `requests==2.32.5` -> `2.33.0`, plus `pygments==2.19.2` advisory pending upstream fix.
- Exit criteria: Update pinned dependency versions where fixes exist, re-run `pip-audit`, and record zero HIGH/CRITICAL unresolved package advisories in baseline tracking.

## Last scan - 2026-03-28 (prj0000091)
- Task: prj0000091-missing-compose-dockerfile
- Lifecycle: OPEN -> IN_PROGRESS -> DONE
- status: DONE
- task_id: prj0000091-missing-compose-dockerfile
- Branch gate: PASS (expected = observed = `prj0000091-missing-compose-dockerfile`)
- Files scanned: `deploy/compose.yaml`, `deploy/Dockerfile.pyagent`, `tests/deploy/test_compose_dockerfile_paths.py`, `docs/project/prj0000091-missing-compose-dockerfile/*`
- Security - CodeQL: SKIPPED (CLI/database flow not invoked; required scoped checks executed)
- Security - ruff S rules: PASS for project scope (repository-wide `src/` run reported pre-existing unrelated findings)
- Security - pip-audit new findings: 0 (`pip_audit_results.json` baseline reports `Deps with vulns: 0`)
- Security - Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security - Workflow injection: PASS (no `.github/workflows/*.yml` changes in this project diff)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (`python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py` -> `2 passed`)
- Quality - Docs vs implementation: PASS (project artifacts complete and aligned)
- Quality - Agent file consistency: PASS
- Findings: 1 MEDIUM (`deploy/Dockerfile.pyagent` non-root user hardening gap), 1 LOW (`ollama:latest` mutable tag)
- Lessons written: 0
- Rules promoted: 0
- Unresolved quality debt: 0 blocking items
- Outcome: CLEAN -> @9git
- handoff_target: @9git

## Unresolved Quality-Debt Ledger
- None open for `prj0000091-missing-compose-dockerfile`.

## Last scan — 2026-03-27 (prj0000088 post-rerun)
- Task: prj0000088-ai-fuzzing-security
- status: DONE
- task_id: prj0000088-ai-fuzzing-security
- Files scanned: `src/core/fuzzing/` (8 files), fuzzing tests (7 files), project docs under `docs/project/prj0000088-ai-fuzzing-security/`, and `docs/architecture/0overview.md`
- Security — CodeQL: SKIPPED (CLI/database flow not invoked in this gate run)
- Security — ruff S rules: PASS with 1 LOW accepted advisory (S311 in `FuzzMutator.py` for deterministic non-crypto PRNG usage)
- Security — mypy strict: PASS (0 findings)
- Security — ruff target scope: PASS (all checks passed)
- Security — pip-audit new findings: 0 (`pip_audit_results.json` baseline reports `Deps with vulns: 0`)
- Security — Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security — Workflow injection: PASS (no `.github/workflows/*.yml` changes in branch diff)
- Quality — Plan vs delivery: PASS
- Quality — AC vs test coverage: PASS (99.06% on `src/core/fuzzing`, threshold 90%)
- Quality — Docs vs implementation: PASS (required project artifacts present and scope docs aligned)
- Quality — Agent file consistency: PASS
- Lessons written: 0
- Rules promoted: 0
- Overall: CLEAN -> @9git
- handoff_target: @9git

## Last scan — 2026-03-27 (prj0000084 rerun after fix/rerun commits)
- Task: prj0000084-immutable-audit-trail
- status: DONE
- task_id: prj0000084-immutable-audit-trail
- Files scanned: `src/core/audit/` (7 files) + audit test suite (7 files including `tests/test_AuditExceptions.py`) + project docs (`project/design/plan/test/code/exec/ql`)
- Security — CodeQL: SKIPPED (CLI not invoked in this rerun; `ruff --select S` executed on changed scope)
- Security — ruff S rules: PASS (0 findings)
- Security — mypy strict: PASS (0 findings)
- Security — ruff target scope: PASS
- Security — pip-audit new findings: 0 (`pip_audit_results.json` baseline: `Deps with vulns: 0`)
- Security — Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security — Workflow injection: PASS (no `.github/workflows/*.yml` changes)
- Quality — Plan vs delivery: PASS
- Quality — AC vs test coverage: PASS (latest @7exec result: 99.36% >= 90)
- Quality — Docs vs implementation: PASS (`tests/test_AuditExceptions.py` now present and aligned across plan/test/code/exec)
- Quality — Agent file consistency: PASS
- Lessons written: 0 (no new recurring pattern)
- Rules promoted: 0
- Overall: CLEAN -> @9git
- handoff_target: @9git

---

## Last scan - 2026-03-27 (prj0000086)
- Task: universal-agent-shell
- task_id: prj0000086-universal-agent-shell
- Status: IN_PROGRESS -> DONE
- Files scanned: `src/core/universal/` (5 files), `tests/test_universal_shell.py`, `tests/test_UniversalIntentRouter.py`, `tests/test_UniversalCoreRegistry.py`, `tests/test_UniversalAgentShell.py`, project docs under `docs/project/prj0000086-universal-agent-shell/`
- Security - CodeQL: SKIPPED (CLI not invoked in this gate; scoped static checks executed)
- Security - ruff S rules: PASS (64x S101 in pytest files only; informational)
- Security - mypy strict: PASS (0 issues)
- Security - ruff full checks: PASS
- Security - Workflow injection: N/A (no `.github/workflows` changes in `origin/main...HEAD` diff)
- Security - pip-audit new findings: 0 in committed baseline (`pip_audit_results.json`)
- Security - Rust unsafe check: SKIPPED (no `rust_core/` changes)
- Quality - Plan vs delivery: PASS
- Quality - AC vs test coverage: PASS (`AC_TEST_NAMES_MISSING=0`; coverage gate 96.26% on `src/core/universal`)
- Quality - Docs vs implementation: PASS (project artifact set complete; scoped docs references consistent)
- Quality - Agent file consistency: PASS
- Lessons written: 0
- Rules promoted: 0
- Overall: CLEAN -> @9git

## Last scan — 2026-03-27 (prj0000083 rerun)
- Task: llm-circuit-breaker (post-fix rerun after 6793030b and 47e589d)
- Files scanned: `src/core/resilience/` (7 files), `tests/test_circuit_breaker.py`, `tests/test_CircuitBreaker*.py`, project docs under `docs/project/prj0000083-llm-circuit-breaker/`
- Security — CodeQL: SKIPPED (CLI not invoked in this rerun)
- Security — ruff S rules: PASS (0 findings)
- Security — mypy strict: PASS (0 issues)
- Security — ruff full checks: PASS
- Security — Workflow injection: N/A (no `.github/workflows` changes in branch diff)
- Security — pip-audit new findings: 0 in committed baseline (`pip_audit_results.json`); live `pip-audit` run failed in venv due missing `cachecontrol` module
- Security — Rust unsafe check: SKIPPED (no `rust_core/` changes)
- Quality — Plan vs delivery: PASS
- Quality — AC vs test coverage: PASS (coverage gate 96.35% on `src/core/resilience`)
- Quality — Docs vs implementation: PASS
- Quality — Agent file consistency: PASS
- Lessons written: 0
- Rules promoted: 0
- Overall: CLEAN -> @9git

---

## Last scan — 2026-03-26 (prj0000080)
- Task: cort-reasoning-pipeline
- Files scanned: `src/core/reasoning/` (4 files) + `tests/unit/test_Cort*.py` + `test_EvaluationEngine.py` (3 files)
- Security — CodeQL: SKIPPED (CLI not invoked; ruff-S used as substitute)
- Security — ruff S rules: PASS (0 findings)
- Security — ruff full config: PASS (0 findings)
- Security — pip-audit new findings: 0 (baseline clean)
- Security — Rust unsafe check: SKIPPED (rust_core/ not changed)
- Security — Workflow injection: N/A (no .github/workflows/ changes)
- Quality — Plan vs delivery: PASS — all 7 required source artifacts present in git diff
- Quality — AC vs test coverage: PASS — 9/9 ACs met (AC-2 name deviation is non-blocking)
- Quality — Docs vs implementation: PASS — all key components confirmed present
- Quality — Agent file consistency: PASS
- Lessons written: 0 (no new recurring patterns)
- Rules promoted: 0
- Advisory: PROMPT_INJECT_V1 — LlmCallable has no guardrails; V2 scope (non-blocking)
- Advisory: QG-1 — ContextTransaction absent; self._active flag used; functionally equivalent

## Last scan — 2026-03-26 (prj0000081)
- Task: mcp-server-ecosystem
- Files scanned: `src/mcp/` (7 files) + `src/tools/tool_registry.py` + `mcp_servers.yml`
- Security — ruff S rules: PASS (0 findings)
- Security — pip-audit new findings: 0 (baseline clean)
- Security — Rust unsafe check: SKIPPED (rust_core/ not changed)
- Security — Workflow injection: N/A (no .github/workflows/ changes)
- Security — Hardcoded secrets: PASS (no secret values in mcp_servers.yml)
- Quality — Plan vs delivery: PASS
- Quality — AC vs test coverage: PASS (33/33 tests, 89.4% coverage)
- Quality — Docs vs implementation: PASS
- Quality — Agent file consistency: PASS
- Findings: 1 HIGH (QL-01: get_event_loop in McpClient.py:124) — FIXED before handoff
- Findings: 1 LOW (QL-02: _response_cache unbounded growth under adversarial flooding) — documented only
- Lessons written: 1 (get_event_loop pattern → 6code.memory.md)
- Rules promoted: 0 (recurrence count 1; threshold 2 not yet reached)
- Overall: CLEAN → @9git
- Overall: CLEAN → @9git

## Last scan — 2026-03-26 (prj0000082)
- Task: agent-execution-sandbox
- Files scanned: `src/core/sandbox/` (5 files) + 5 test files
- Security — ruff S rules: PASS (4× S101 in validate() helpers — INFO, intentional codebase pattern)
- Security — mypy --strict: PASS (0 errors)
- Security — pip-audit new findings: 0 (baseline clean; cachecontrol module missing so live audit skipped; baseline read from committed json)
- Security — Rust unsafe check: SKIPPED (rust_core/ not changed)
- Security — Workflow injection: N/A (no .github/workflows/ changes)
- Security — Path traversal (A05): PASS — resolve() before comparison, validate-before-I/O enforced on all 4 operations, empty allowlist = deny-all
- Security — SSRF / host injection (A03/A10): PASS — exact-match allowlist, no bypass via crafted strings
- Quality — Plan vs delivery: PASS — all 5 source files + 5 test files present; test count exceeded (32 vs 19 planned)
- Quality — AC vs test coverage: PASS — 19/19 ACs covered; 100% module coverage
- Quality — Docs vs implementation: PASS — minor _is_subpath design drift (module-level func vs @staticmethod) is functionally equivalent
- Quality — Agent file consistency: PASS
- Findings: 0 CRITICAL, 0 HIGH, 0 MEDIUM
- Findings: 1 LOW — allowlist paths exposed in SandboxViolationError.reason field (informational, no bypass possible)
- Findings: 4 INFO — S101 assert in validate() helpers (intended pattern)
- Lessons written: 1 (allowlist exposure in error reason field — new, recurrence 1)
- Rules promoted: 0 (recurrence count 1; threshold 2 not yet reached)
- Overall: CLEAN → @9git

## Lesson — 2026-03-26 (prj0000082)
**Pattern:** `SandboxViolationError.reason` exposes allowlist contents
**Root cause:** `_validate_path()` includes `self._sandbox.allowed_paths` in the reason string for debugging convenience. In a multi-agent environment this gives an untrusted agent knowledge of all allowed directories upon triggering a violation.
**Prevention:** Error reason should be static: `"path not in allowed_paths"` — omit the list. The rejected path (`resource`) already tells the caller what was attempted without revealing the full allowlist.
**First seen:** prj0000082
**Recurrence count:** 1

## Promotions
_(none yet)_

## Last scan — 2026-03-27 (prj0000084)
- Task: prj0000084-immutable-audit-trail
- Files scanned: `src/core/audit/` (7 files) + audit test suite (6 files) + project docs (`project/design/plan/test/code/exec/ql`)
- Security — CodeQL: SKIPPED (CLI not invoked in this run; `ruff --select S` executed)
- Security — ruff S rules: PASS (0 findings)
- Security — mypy strict: PASS (0 findings)
- Security — ruff full target scope: PASS
- Security — pip-audit new findings: 0 (committed baseline in `pip_audit_results.json` reports 0 vulnerable dependencies)
- Security — Rust unsafe check: SKIPPED (`rust_core/` not modified)
- Security — Workflow injection: N/A (no workflow file changes)
- Quality — Plan vs delivery: PASS (core audit files + planned artifacts present)
- Quality — AC vs test coverage: FAIL (83.07% < required 90%)
- Quality — Docs vs implementation: FAIL (plan references missing `tests/test_AuditExceptions.py`; exec PASS label inconsistent with coverage threshold)
- Quality — Agent file consistency: PASS (no recurrence promotion triggered)
- Lessons written: 2 (coverage gate miss, missing test-file reference -> `5test.memory.md`)
- Rules promoted: 0
- Overall: BLOCKED -> @5test



---

## prj0000078 — pm-swot-risk-ui

| Field | Value |
|---|---|
| **task_id** | prj0000078-pm-swot-risk-ui |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-26 |
| **status** | DONE |
| **branch** | prj0000078-pm-swot-risk-ui |
| **files_scanned** | `web/apps/ProjectManager.tsx`, `web/apps/ProjectManager.test.tsx`, `web/vite-env.d.ts` |
| **security_ruff_s** | PASS — 54 pre-existing baseline findings in src/; 0 new findings |
| **security_ts_xss** | PASS — `<pre>` text-child rendering; no dangerouslySetInnerHTML |
| **security_ts_path** | PASS — build-time Vite static import; no runtime path construction |
| **security_ts_events** | PASS — useEffect with proper removeEventListener cleanup |
| **security_ts_proto** | PASS — extractSection uses indexOf/slice with hardcoded heading literals |
| **security_npm_deps** | PASS — web/package.json unchanged; no new packages |
| **quality_plan** | PASS — all code deliverables confirmed in git diff |
| **quality_ac** | PASS — all 8 ACs satisfied |
| **quality_docs** | PASS — scope deviation (no Editor/App.tsx changes) is valid S-budget simplification |
| **structure_tests** | PASS — 129/129 |
| **summary** | 0 CRITICAL, 0 HIGH, 0 MEDIUM, 0 LOW. 2 INFO-level quality observations (non-blocking). All 8 ACs satisfied. 129 structure tests pass. CLEAR for @9git. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj0000078/pm-swot-risk-ui.ql.md |

---

## prj0000047 — conky-real-metrics

| Field | Value |
|---|---|
| **task_id** | prj0000047-conky-real-metrics |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-23 |
| **status** | DONE |
| **branch** | prj0000047-conky-real-metrics ✓ |
| **files_scanned** | `backend/app.py`, `web/apps/Conky.tsx`, `tests/test_backend_system_metrics.py` |
| **codeql** | SKIPPED (CLI not invoked) |
| **ruff_S** | PASS (0 findings) |
| **pip_audit** | PASS — psutil 7.2.1, vulns:[] |
| **rust_unsafe** | SKIPPED (rust_core not changed) |
| **block_items** | 0 |
| **warn_items** | 3 × LOW/MEDIUM (info-disclosure, no rate-limit, no auth) |

---

## prj0000075 — ci-simplification

| Field | Value |
|---|---|
| **task_id** | prj0000075-ci-simplification |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-25 |
| **status** | DONE |
| **branch** | prj0000075-ci-simplification ✓ |
| **files_scanned** | `.github/workflows/security.yml`, `tests/ci/test_workflow_count.py`, `tests/structure/test_ci_yaml.py`, `docs/setup.md`, `pyproject.toml` |
| **security_workflow_injection** | PASS — no user-controlled data in run steps; static matrix only |
| **security_trigger** | PASS — `pull_request` used, not `pull_request_target` |
| **security_permissions** | PASS — minimal: contents:read, security-events:write, actions:read |
| **security_action_pinning** | LOW — version tags used for GitHub-owned actions (acceptable) |
| **ruff_S** | PASS (0 findings) |
| **pip_audit** | PASS — 0/253 deps with CVEs |
| **rust_unsafe** | SKIPPED (rust_core not changed) |
| **quality_plan_vs_delivery** | PASS — all 5 tasks delivered |
| **quality_ac_vs_tests** | PASS — 5 ACs, 5 corresponding tests |
| **quality_docs_vs_impl** | PASS — setup.md commands verified |
| **quality_agent_consistency** | PASS |
| **block_items** | 0 |
| **lessons_written** | 3 (I001 import sort → 6code; deprecated ruff config → 6code; D203/D213 conflict → 6code) |
| **rules_promoted** | 0 (first occurrence each; threshold is 2) |

## Promotions
_(none yet — all lessons at recurrence count 1; promote at count 2)_
| **overall** | CLEAN → @9git |
| **artifact_paths** | docs/project/prj0000047/conky-real-metrics.ql.md |

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Markdown-only changes to 9 *.agent.md files. No secrets, injection patterns, data-exfil URLs, or path traversal found. No Python/Rust files modified. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/agent-doc-frequency.ql.md |

---

## prj008 - agent_workflow

| Field | Value |
|---|---|
| **task_id** | prj008-agent_workflow |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | 2 LOW findings (S101 assert in validate()). Both false positives — internal contract guards only. 0 CRITICAL/HIGH. CLEAR for @9git. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj008-agent_workflow/agent_workflow.ql.md |

---

## prj007 - advanced_research

| Field | Value |
|---|---|
| **task_id** | prj007-advanced_research |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | 0 findings across all 5 skeleton packages. Placeholder modules — no subprocess, no secrets, no IO. CLEAR for @9git. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj007-advanced_research/advanced_research.ql.md |

---

## prj006 - unified-transaction-manager

| Field | Value |
|---|---|
| **task_id** | prj006-unified-transaction-manager |
| **owner_agent** | @8ql |
| **source** | @7exec |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | 0 CRITICAL, 0 HIGH, 0 MEDIUM. 6 LOW/INFO findings all false positives (S603/S607 on subprocess with fully-resolved Rust binary paths; S101 assert in pytest files). pip-audit: 0 new CVEs. CLEAR for @9git. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj006-unified-transaction-manager/unified-transaction-manager.ql.md |
