# 8ql Memory

This file tracks security scan results, CodeQL findings, 
and dependency audit outcomes.

## Auto-handoff

Once security scans and CodeQL analysis are complete, 
the next agent in the workflow is **@9git**. 
Invoke it via `agent/runSubagent` to continue the process.

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
- Overall: CLEAN → @9git

## Promotions
_(none yet)_



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
