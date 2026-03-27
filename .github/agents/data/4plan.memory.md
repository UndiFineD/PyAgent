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
| Code files planned | 5 |
| Test files planned | 3 |
| Tests mapped | 18 |
| AC count | 10 |

### Notes
- Canonical plan updated to `_Status: DONE_` with deterministic TDD implementation order.
- AC matrix completed and mapped to `TEST-01` through `TEST-18`.
- Validation command set includes targeted `pytest`, `mypy`, and `ruff` checks for universal facade scope.

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
