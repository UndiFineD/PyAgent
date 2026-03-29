# 4plan Memory

This file tracks implementation plans, 
task breakdowns, and progress checklists.

## Auto-handoff

Once an implementation plan is ready and validated, 
the next agent in the workflow is **@5test**.

To invoke the next agent, use the following command:

- `agent/runSubagent @5test`

This ensures the plan is handed off cleanly to the testing phase, 
where test cases are written and validated against the plan.

---

## prj0000093 - projectmanager-ideas-autosync

| Field | Value |
|---|---|
| **task_id** | prj0000093-projectmanager-ideas-autosync |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.plan.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md |
| **branch** | prj0000093-projectmanager-ideas-autosync (validated PASS before artifact writes) |

### Chunk 001 Summary

| Item | Value |
|---|---|
| Code files planned | 3-5 |
| Test files planned | 3-5 |
| Task IDs | T1-T7 |
| Scope | `/api/ideas` backend contract, idea parsing/mapping helpers, ProjectManager Active Ideas panel, backend/frontend TDD coverage, milestone/doc updates |

### Acceptance Coverage

| Task | Acceptance IDs |
|---|---|
| T1 | AC-04 |
| T2 | AC-02, AC-03, AC-04 |
| T3 | AC-01, AC-07 |
| T4 | AC-02, AC-03, AC-04, AC-07 |
| T5 | AC-05, AC-06 |
| T6 | AC-05, AC-06 |
| T7 | AC-08 |

### Dependency Order
1. T1 -> T2 -> T3
2. T4 defines TDD gate before @6code implementation for backend contract tasks.
3. T5 -> T6
4. T7 closes milestone/status and records handoff readiness.

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Planning quality improves when every task embeds objective, concrete file list, acceptance, and executable validation command. |
| Root cause | Prior shallow plans with generic task labels created ambiguity for @5test/@6code handoff and delayed execution sequencing. |
| Prevention | Enforce hard-task schema (objective + files + acceptance + command) and explicit dependency chain in canonical plan before status transition. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Produced T0–T9 task list for patching all 9 *.agent.md files with checkpoint rule + inline artifact template. No Python code. @5test skipped. |
| **handoff_target** | @6code |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/agent-doc-frequency.plan.md |

---

## prj0000052 — project-management

| Field | Value |
|---|---|
| **task_id** | prj0000052-project-management |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-24 |
| **updated_at** | 2026-03-24 |
| **status** | DONE |
| **handoff_target** | @0master (report back — no @5test handoff per instructions) |
| **artifact_paths** | docs/project/prj0000052/project-management.plan.md |
| **branch** | prj0000052-project-management (verified before write) |

### Tasks (single chunk)

| Task | File(s) | AC | Notes |
|---|---|---|---|
| T1 | data/projects.json | AC-01 | 62-entry JSON array |
| T2 | docs/project/kanban.md | AC-02 | 7-lane board, 62 rows |
| T3 | backend/app.py | AC-05 | GET /api/projects + ProjectModel |
| T4 | web/apps/ProjectManager.tsx | AC-03 | NebulaOS kanban app |
| T5 | web/src/App.tsx, web/src/types.ts | AC-04 | Register projectmanager AppId |
| T6 | .github/agents/0master.agent.md | AC-06 | kanban.md lifecycle section |
| T7 | .github/agents/1project.agent.md | AC-06 | kanban.md lifecycle convention |

### Test file
`tests/structure/test_kanban.py` — 15 tests for AC-01 + AC-02

---

## prj0000045 — transaction-managers-full

| Field | Value |
|---|---|
| **task_id** | prj0000045-transaction-managers-full |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-22 |
| **updated_at** | 2026-03-22 |
| **status** | HANDED_OFF |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000045/transaction-managers-full.plan.md |
| **branch** | prj0000045-transaction-managers-full (plan authored on main — branch gate for @6code/@9git) |

### Chunk 1 (all tasks — single chunk)

| Task | File(s) | Type | Acceptance milestone |
|---|---|---|---|
| T00 | requirements.txt | EDIT | `cryptography>=42.0.0` declared |
| T01 | src/transactions/__init__.py | NEW | package importable |
| T02 | src/transactions/BaseTransaction.py | NEW | ABC enforced |
| T03 | src/transactions/StorageTransactionManager.py | NEW | dual-mode + encrypt |
| T04 | src/transactions/ProcessTransactionManager.py | NEW | _proc.poll, stdout capture |
| T05 | src/transactions/ContextTransactionManager.py | NEW | UUID lineage, RecursionGuardError |
| T06 | src/transactions/MemoryTransactionManager.py | NEW | RLock+asyncio.Lock, sync_remote |
| T07 | src/core/StorageTransactionManager.py | NEW shim | re-export + validate |
| T08 | src/core/ProcessTransactionManager.py | NEW shim | re-export + validate |
| T09 | src/core/ContextTransactionManager.py | NEW shim | re-export + validate + RecursionGuardError |
| T10 | src/MemoryTransactionManager.py | EDIT→shim | re-export + validate |
| T11 | tests/test_StorageTransactionManager.py | NEW test | async API + encrypt fixture |
| T12 | tests/test_ProcessTransactionManager.py | NEW test | async run/rollback |
| T13 | tests/test_ContextTransactionManager.py | NEW test | UUID lineage + current() |
| T14 | — | validate | pytest 14+new pass |

### Key resolved decisions
- `commit()` is sync only (no asyncio.run); `__aexit__` calls sync commit — no event-loop conflict
- Concrete managers do NOT inherit BaseTransaction (duck typing; avoids sync/async method name clash)
- `ProcessTransaction.wait()` uses `.communicate()` not `.wait()` — captures `self.stdout`
- All `src/core/` shims are NEW files (none existed before this project)
- `cryptography>=42.0.0` added to requirements.txt; httpx already present at 0.28.1

---

## prj0000047 — conky-real-metrics

| Field | Value |
|---|---|
| **task_id** | prj0000047-conky-real-metrics |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-23 |
| **updated_at** | 2026-03-23 |
| **status** | HANDED_OFF |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000047/conky-real-metrics.plan.md |
| **branch** | prj0000047-conky-real-metrics (validated ✅) |

### Chunk 1 (all tasks — single chunk)

| Task | File(s) | Type | Acceptance |
|---|---|---|---|
| T1 | backend/requirements.txt | EDIT | `psutil>=5.9` present |
| T2 | backend/app.py | EDIT | 4 Pydantic models importable |
| T3 | backend/app.py | EDIT | endpoint returns HTTP 200; first-call KB/s == 0.0 |
| T4 | tests/test_backend_system_metrics.py | NEW TEST | 6 unit tests green |
| T5 | web/apps/Conky.tsx | EDIT | TS interfaces + hook added; `npx tsc --noEmit` passes |
| T6 | web/apps/Conky.tsx | EDIT | no Math.random(); OFFLINE badge; disk row; real data |
| T7 | — | VALIDATE | full pytest suite + tsc clean |

### Key design decisions carried forward
- `useSystemMetrics` inline in `Conky.tsx` (not extracted to a separate hook file)
- First-call `cpu_percent: 0.0` accepted (no startup prime call)
- `_prev_net / _prev_disk` module-level state (safe for single-worker Uvicorn)
- No `vite.config.ts` changes required
- OFFLINE badge: `text-red-500/50 text-[9px]`; stays on last values when offline


---

## prj0000092 - mypy-strict-enforcement

| Field | Value |
|---|---|
| **task_id** | prj0000092-mypy-strict-enforcement |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.plan.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.project.md |
| **branch** | prj0000092-mypy-strict-enforcement (validated PASS before artifact write) |

### Chunk 001 Summary

| Item | Value |
|---|---|
| Code/config files planned | 3 |
| Test files planned | 4 |
| Task IDs | T1-T7 |
| Scope | phase-1 strict lane config, CI strict command wiring, structure + smoke guardrails |

### Acceptance Coverage
| Task | Acceptance IDs |
|---|---|
| T1 | AC-001, AC-002, AC-004 |
| T2 | AC-003, AC-004 |
| T3 | AC-005 |
| T4 | AC-001, AC-002 |
| T5 | AC-003 |
| T6 | AC-006 |
| T7 | AC-001, AC-002, AC-003, AC-004, AC-005, AC-006 |

### Dependency Order
1. T1 -> T2 -> T3
2. TDD gate to @6code: T4/T5/T6 begin only after @5test establishes failing tests for T1/T2/T3.
3. T7 runs after implementation is green and records scope/evidence for @7exec.

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Strict-lane rollout planning is most stable when config, CI contract, and fixture-backed smoke checks are planned as one dependency chain. |
| Root cause | Previous type-policy efforts drifted because one of the three guardrail layers (config, CI, or tests) was under-specified. |
| Prevention | Require every strictness plan to include exact allowlist lock tests, blocking CI assertion tests, and a deterministic failing fixture smoke test. |
| First seen | 2026-03-28 |
| Seen in | prj0000092-mypy-strict-enforcement |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

---

## prj0000076 — future-ideas-kanban

| Field | Value |
|---|---|
| **task_id** | prj0000076-future-ideas-kanban |
| **owner_agent** | @4plan |
| **source** | @2think (design SKIPPED) |
| **created_at** | 2026-03-26 |
| **updated_at** | 2026-03-26 |
| **status** | DONE |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj0000076/prj0000076.plan.md, docs/project/kanban.md |
| **branch** | prj0000076-future-ideas-kanban (validated ✅) |
| **commit** | d8ea03326 |

### Summary
Documentation-only project. No source code, tests, or CI changes. @4plan wrote the
`## Future Ideas` section directly into `docs/project/kanban.md` (38 ideas, 9 areas,
P1–P4 priorities, SWOT classification for P1/P2). All agents M2/M4/M5/M6/M7 SKIPPED.
Ready for @9git handoff.

---

## prj0000096 - coverage-minimum-enforcement

| Field | Value |
|---|---|
| **task_id** | prj0000096-coverage-minimum-enforcement |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.plan.md, docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.project.md |
| **branch** | prj0000096-coverage-minimum-enforcement (validated PASS before artifact write) |

### Chunk 001 Summary

| Item | Value |
|---|---|
| Code/config/docs files planned | 3-4 |
| Test files planned | 2 |
| Task IDs | T1-T5 |
| Scope | Stage-1 coverage minimum enforcement (40) with blocking CI gate, TDD guardrails, and rollout evidence format |

### Acceptance Coverage

| Task | Acceptance IDs |
|---|---|
| T1 | AC-001, AC-004 |
| T2 | AC-002, AC-003 |
| T3 | AC-001, AC-004, AC-005 |
| T4 | AC-002, AC-003 |
| T5 | AC-003, AC-006 |

### Dependency Order
1. T1 -> T2
2. T1/T2 complete in @5test before @6code implementation starts.
3. T3 -> T4 -> T5

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | First-slice planning is most executable when each task explicitly carries exact files, acceptance checks, and one PowerShell validation command. |
| Root cause | Placeholder plans without per-task file/command detail create ambiguous @5test/@6code boundaries and inconsistent TDD sequencing. |
| Prevention | Enforce the hard-task schema in canonical plan output and reject tasks lacking file targets or executable validation commands. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync; prj0000096-coverage-minimum-enforcement |
| Recurrence count | 2 |
| Promotion status | PROMOTED_TO_HARD_RULE |

---

## prj0000090 - private-key-remediation

| Field | Value |
|---|---|
| **task_id** | prj0000090-private-key-remediation |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.plan.md |
| **branch** | prj0000090-private-key-remediation (validated PASS before artifact write) |

### Chunk Plan Summary

| Chunk | Code files planned | Test files planned | Task IDs |
|---|---:|---:|---|
| Chunk 001 - Guardrails + Rotation Gate | 8 | 8 | T1-T8 |
| Chunk 002 - Rewrite + Governance Completion | 8 | 7 | T9-T16 |

### Dependency Order
1. Chunk 001: T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8
2. Chunk 002: T9 -> T10 -> T11 -> T12 -> T13 -> T14 -> T15 -> T16
3. TDD gate: @6code implementation tasks must wait for @5test failing tests in paired order.

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Secret-remediation plans need explicit rollback gates per phase, not only end-state checks. |
| Root cause | Prior plans often captured verification commands but omitted operational rollback triggers for rewrite workflows. |
| Prevention | Add mandatory checkpoint table with required signal + rollback action for containment, rotation gate, rewrite, and stabilization. |
| First seen | 2026-03-28 |
| Seen in | prj0000090-private-key-remediation |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

---

## prj0000088 — ai-fuzzing-security

| Field | Value |
|---|---|
| **task_id** | prj0000088-ai-fuzzing-security |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.plan.md |
| **branch** | prj0000088-ai-fuzzing-security (validated) |

### Chunk 001 Summary

| Item | Value |
|---|---|
| Code files planned | 8 |
| Test files planned | 7 |
| Tests mapped | 18 |
| AC count | 10 |

### Dependency Order
1. T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8
2. T8 remains blocked until tests for T1-T7 exist and fail first (TDD gate).

### Notes
- Canonical plan updated to `_Status: DONE_`.
- AC matrix completed and mapped to TEST-01 through TEST-18.
- Validation commands include targeted pytest, mypy, and ruff checks.

---

## prj0000086 — universal-agent-shell

| Field | Value |
|---|---|
| **task_id** | prj0000086-universal-agent-shell |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000086-universal-agent-shell/universal-agent-shell.plan.md |
| **branch** | prj0000086-universal-agent-shell (validated ✅) |

### Chunk 001 Summary

| Item | Value |
|---|---|

---

## prj0000091 - missing-compose-dockerfile

| Field | Value |
|---|---|
| **task_id** | prj0000091-missing-compose-dockerfile |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.plan.md |
| **branch** | prj0000091-missing-compose-dockerfile (validated PASS before artifact write) |

### Chunk 001 Summary

| Item | Value |
|---|---|
| Code files planned | 2 |
| Test files planned | 1 |
| Task IDs | T1-T5 |
| Scope | compose Dockerfile path fix + deploy Dockerfile addition + regression guard tests |

### Dependency Order
1. T1 -> T2 -> T3 -> T4 -> T5
2. TDD gate: @6code implementation begins only after @5test adds failing tests for T1-T3 contracts.

### Acceptance Coverage
| Task | Acceptance IDs |
|---|---|
| T1 | AC-001, AC-002 |
| T2 | AC-003 |
| T3 | AC-004 |
| T4 | AC-005 |
| T5 | AC-006 |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Small deploy path fixes benefit from a static-path regression test before optional docker build smoke. |
| Root cause | Missing Dockerfile path escaped earlier because compose config validity was not asserted in tests. |
| Prevention | Require deterministic compose `build.dockerfile` existence checks in targeted deploy tests for each compose service. |
| First seen | 2026-03-28 |
| Seen in | prj0000091-missing-compose-dockerfile |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

### Notes
- Canonical plan updated to `_Status: DONE_` with deterministic TDD implementation order.
- Validation commands include targeted pytest and compose checks for this deploy-scope project.

---

## prj0000076 — future-ideas-kanban

| Field | Value |
|---|---|
| **task_id** | prj0000076-future-ideas-kanban |
| **owner_agent** | @4plan |
| **source** | @2think (design SKIPPED) |
| **created_at** | 2026-03-26 |
| **updated_at** | 2026-03-26 |
| **status** | DONE |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj0000076/prj0000076.plan.md, docs/project/kanban.md |
| **branch** | prj0000076-future-ideas-kanban (validated ✅) |
| **commit** | d8ea03326 |

### Summary
Documentation-only project. No source code, tests, or CI changes. @4plan wrote the
`## Future Ideas` section directly into `docs/project/kanban.md` (38 ideas, 9 areas,
P1–P4 priorities, SWOT classification for P1/P2). All agents M2/M4/M5/M6/M7 SKIPPED.
Ready for @9git handoff.
