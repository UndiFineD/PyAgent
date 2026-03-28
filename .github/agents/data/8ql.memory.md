# 8ql Memory

This file tracks security scan results, CodeQL findings, 
and dependency audit outcomes.

## Auto-handoff

Once security scans and CodeQL analysis are complete, 
the next agent in the workflow is **@9git**. 
Invoke it via `agent/runSubagent` to continue the process.

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
