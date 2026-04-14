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

## prj0000099 - stub-module-elimination

| Field | Value |
|---|---|
| **task_id** | prj0000099-stub-module-elimination |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | IN_PROGRESS |
| **lifecycle** | OPEN -> IN_PROGRESS |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.plan.md, docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md, docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md, docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.exec.md, docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.ql.md, docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.git.md |
| **branch** | prj0000099-stub-module-elimination (validated PASS before artifact writes) |

### Actionable Tasks

| Task | Objective | Validation command |
|---|---|---|
| T1 | Verify non-empty package APIs for target packages | `python -c "from pathlib import Path; fs=['src/rl/__init__.py','src/speculation/__init__.py','src/cort/__init__.py','src/runtime_py/__init__.py','src/runtime/__init__.py','src/memory/__init__.py']; bad=[f for f in fs if not any(l.strip() and not l.strip().startswith('#') for l in Path(f).read_text(encoding='utf-8').splitlines())]; print('PASS' if not bad else 'FAIL:' + ','.join(bad)); raise SystemExit(1 if bad else 0)"` |
| T2 | Run focused tests for targeted package surfaces | `python -m pytest -q tests/test_rl_package.py tests/test_speculation_package.py tests/test_cort.py tests/test_memory_package.py tests/test_runtime.py` |
| T3 | Record code/test/exec/ql artifacts with execution evidence | `rg -n "_Status:|Validation Results|Run Log|Findings|Cleared" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.exec.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.ql.md` |
| T4 | Update milestones and complete @9git handoff packet | `rg -n "Milestone|M8|@9git|_Status:" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.plan.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.git.md` |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Validation-first closure plans stay executable when each closure task includes explicit file scope and command-level proof. |
| Root cause | Placeholder plan content without concrete targets/commands blocked deterministic handoff. |
| Prevention | Enforce task schema: objective, target files, acceptance, and validation command per task. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync; prj0000099-stub-module-elimination |
| Recurrence count | 2 |
| Promotion status | PROMOTED_TO_HARD_RULE |

---

## prj0000098 - backend-health-check-endpoint

| Field | Value |
|---|---|
| **task_id** | prj0000098-backend-health-check-endpoint |
| **owner_agent** | @4plan |
| **source** | @3design (using @2think recommendation because design artifact is placeholder) |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.plan.md |
| **branch** | prj0000098-backend-health-check-endpoint (validated PASS before artifact writes) |

### Slice 1 Summary

| Item | Value |
|---|---|
| Scope | `/health`, `/livez`, `/readyz` backend endpoint and related tests only |
| Out of scope guard | No startup state machine, no dependency probes, no frontend changes |
| Task IDs | T1-T6 |
| Test-first sequence | T1-T3 (@5test red) before T4-T6 (@6code green) |

### Acceptance Coverage

| Task | Acceptance IDs |
|---|---|
| T1 | AC-001, AC-002, AC-003 |
| T2 | AC-004 |
| T3 | AC-005 |
| T4 | AC-001, AC-002, AC-003, AC-004 |
| T5 | AC-005 |
| T6 | AC-001, AC-002, AC-003, AC-004, AC-005 |

### Dependency Order
1. T1 -> T2 -> T3
2. T4 depends on T1-T3
3. T5 depends on T3 and can run with T4
4. T6 depends on T4-T5

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Endpoint-slice plans are handoff-safe when red tasks and green tasks are split explicitly by agent with per-task validation commands. |
| Root cause | Prior health endpoint requests risked ambiguous execution ownership between @5test and @6code when tasks were not phase-labeled. |
| Prevention | Require every slice task to name owner phase (@5test red or @6code green), file list, and command-level pass criteria. |
| First seen | 2026-03-29 |
| Seen in | prj0000098-backend-health-check-endpoint |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

---

## 2026-04-04 rollover - current.4plan.memory.md reset for prj0000122

- Archived current-memory coverage for completed planning projects `prj0000104`, `prj0000105`, `prj0000106`, `prj0000107`, `prj0000108`, `prj0000109`, `prj0000110`, `prj0000114`, `prj0000115`, `prj0000116`, `prj0000117`, `prj0000118`, and `prj0000120` before opening `prj0000122-jwt-refresh-token-support`.
- Preserved active hard-rule lessons: every task must include objective, target files, acceptance criteria, owner, and at least one deterministic validation command; conclusive gate evidence is required before DONE.

---

## prj0000097 - stub-module-elimination

| Field | Value |
|---|---|
| **task_id** | prj0000097-stub-module-elimination |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.plan.md |
| **branch** | prj0000097-stub-module-elimination (validated PASS before artifact writes) |

### Slice 1 Summary

| Item | Value |
|---|---|
| Scope | `rl` + `speculation` implementation/test guardrails only |
| Out of scope guard | No edits to `runtime*`, `memory*`, `cort*` implementation files |
| Task IDs | T1-T8 |
| Test-first sequence | T1-T5 (@5test) before T6-T8 (@6code) |

### Acceptance Coverage

| Task | Acceptance IDs |
|---|---|
| T1 | AC-001 |
| T2 | AC-002 |
| T3 | AC-003, AC-004 |
| T4 | AC-005 |
| T5 | AC-006 |
| T6 | AC-001, AC-002, AC-005 |
| T7 | AC-003, AC-004, AC-005 |
| T8 | AC-006, AC-007, AC-008 |

### Dependency Order
1. T1 -> T2 -> T3 -> T4 -> T5
2. T6 depends on T1-T2 (RL path)
3. T7 depends on T3-T4 (speculation path)
4. T8 depends on T5-T7 (inventory and scope closure)

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Plans are execution-safe when each task has objective, files, AC IDs, and a validation command. |
| Root cause | Generic tasks without file scope and command checks caused handoff ambiguity. |
| Prevention | Enforce hard-task schema and targeted-then-broader validation gates before handoff. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync; prj0000097-stub-module-elimination |
| Recurrence count | 2 |
| Promotion status | PROMOTED_TO_HARD_RULE |

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

---

## prj0000100 - repo-cleanup-docs-code

| Field | Value |
|---|---|
| **task_id** | prj0000100-repo-cleanup-docs-code |
| **owner_agent** | @4plan |
| **source** | @3design |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **handoff_target** | @5test |
| **artifact_paths** | docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.plan.md, docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md |
| **branch** | prj0000100-repo-cleanup-docs-code (validated PASS before artifact writes) |

### Chunk Boundaries

| Chunk | Scope | Planned File Volume |
|---|---|---|
| C1 | Governance protocol lock (codestructure + allowed websites + guidance) | ~4-8 code/docs, ~2-4 tests |
| C2 | Docs cleanup + lifecycle tracking sync | ~8-12 code/docs, ~4-6 tests |
| C3 | Bounded code cleanup wave | ~8-12 code files, ~6-10 tests |
| C4 | Closure evidence + handoff | ~2-4 docs, ~1-2 tests |

### Acceptance Coverage

| Task | Acceptance IDs |
|---|---|
| T1 | AC-03, AC-04, AC-05 |
| T2 | AC-03 |
| T3 | AC-04, AC-05 |
| T4 | AC-01, AC-02 |
| T5 | AC-01, AC-02 |
| T6 | AC-01 |
| T7 | AC-01, AC-05 |
| T8 | AC-01, AC-02, AC-03, AC-04, AC-05 |

### Dependency Order
1. T1 -> T2 -> T3
2. T4 || T5 after T1-T3
3. T6 after T1-T3 and in bounded batches
4. T7 after each cleanup batch
5. T8 finalizes closure and handoff packet

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Governance-first cleanup plans remain executable when policy contracts, docs waves, and code waves are split into phased tasks with explicit file scope and command-level checks. |
| Root cause | Placeholder planning artifacts and missing AC mapping create handoff ambiguity and weak verification coverage for cleanup-heavy projects. |
| Prevention | Enforce hard task schema (objective, target files, acceptance criteria, validation command) plus AC traceability matrix in the canonical plan. |
| First seen | 2026-03-29 |
| Seen in | prj0000100-repo-cleanup-docs-code |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |
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


--- Appended from current ---

# Current Memory - 4plan

## Metadata
- agent: @4plan
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.4plan.memory.md in chronological order, then clear Entries.

## prj0000127 - mypy-strict-enforcement

| Field | Value |
|---|---|
| task_id | prj0000127-mypy-strict-enforcement |
| owner_agent | @4plan |
| source | user request + `mypy-strict-enforcement.project.md` + `mypy-strict-enforcement.think.md` + `mypy-strict-enforcement.design.md` + `mypy.ini` + `pyproject.toml` |
| created_at | 2026-04-04 |
| updated_at | 2026-04-04 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Chunk A warn-phase planning tasks `T-MYPY-001..T-MYPY-006`; Chunk B required-phase planning tasks `T-MYPY-007..T-MYPY-010` |
| acceptance_criteria_scope | Strict command contract, config authority contract, allowlist drift control, warn->required promotion threshold, rollback taxonomy checkpoints |
| dependency_order | `T-MYPY-001 || T-MYPY-002` -> `T-MYPY-003` -> `T-MYPY-004 || T-MYPY-005` -> `T-MYPY-006` -> `T-MYPY-007` -> `T-MYPY-008` -> `T-MYPY-009` -> `T-MYPY-010` |
| handoff_target | @5test |
| artifact_paths | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.plan.md` |
| branch | prj0000127-mypy-strict-enforcement (validated PASS before artifact writes) |
| first_red_slice | `T-MYPY-001` on `tests/docs/test_agent_workflow_policy_docs.py` with selector `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or mypy"` |
| validation_evidence | pending run in current session (docs policy selector) |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Phased type-enforcement plans are most reliable when warn and required gates are modeled as separate milestones with explicit rollback checkpoints. |
| Root cause | Plans that skip mode-transition contracts tend to mix advisory and blocking behavior, creating ambiguous execution ownership between @6code and @7exec. |
| Prevention | Require per-task mode labels (RED/GREEN/EXEC), explicit promotion thresholds, and lane-level rollback criteria in the initial plan artifact. |
| First seen | 2026-04-04 |
| Seen in | prj0000127-mypy-strict-enforcement |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

## prj0000125 - llm-gateway-lessons-learned-fixes

| Field | Value |
|---|---|
| task_id | prj0000125-llm-gateway-lessons-learned-fixes |
| owner_agent | @4plan |
| source | user request + design.md (4 waves) + project.md + gateway_core.py + test_gateway_core_orchestration.py + ADR-0009 |
| created_at | 2026-04-04 |
| updated_at | 2026-04-04 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Single plan file (6 tasks total: T-LGW2-001..T-LGW2-006) |
| wave_a_tasks | T-LGW2-001 (RED: budget_denied), T-LGW2-002 (RED: provider_exception), T-LGW2-003 (RED: degraded_telemetry), T-LGW2-004 (GREEN: fail-closed handle()) |
| wave_b_tasks | T-LGW2-005 (RED: ordering skeleton), T-LGW2-006 (GREEN: event_log fixture) |
| wave_c_status | DONE — completed in commit 1c16acfde6; rg NOT_STARTED docs/project/prj0000124-llm-gateway/ returns 0 matches; ADR 0009 Part 2 present |
| wave_d_status | DONE — decision recorded in design.md; gateway_core.py snake_case COMPLIANT; no rename |
| acceptance_criteria_scope | AC-A1, AC-A2, AC-A3, AC-B1, AC-B2 (C1/C2/D1 already satisfied) |
| dependency_order | T-LGW2-001 + T-LGW2-002 + T-LGW2-003 (parallel) -> T-LGW2-004; T-LGW2-005 -> T-LGW2-006; convergence: T-LGW2-004 + T-LGW2-006 -> @7exec |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.plan.md |
| commit_sha | af64828b3f |
| branch | prj0000125-llm-gateway-lessons-learned-fixes (PASS) |
| governance_gate | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 17 passed |
| first_red_slice | T-LGW2-001: test_budget_denied_does_not_call_provider in tests/core/gateway/test_gateway_core_orchestration.py |

### @5test Handoff Directive

Start with all 4 RED tasks in a single session (parallel-safe, independent test functions):
- T-LGW2-001: `test_budget_denied_does_not_call_provider` — budget allowed=False must block provider execution
- T-LGW2-002: `test_provider_exception_returns_failed_result` — provider raise must return failed result without propagation
- T-LGW2-003: `test_degraded_telemetry_result_still_returned` — emit_result raise must return with telemetry.degraded=True
- T-LGW2-005: `test_event_log_ordering_detects_reversed_execution` — shared event_log skeleton (stubs not yet wired, so FAILS)

All four tests must FAIL against the current gateway_core.py before handoff to @6code.



| Field | Value |
|---|---|
| task_id | prj0000124-llm-gateway |
| owner_agent | @4plan |
| source | user request + `llm-gateway.project.md` + `llm-gateway.think.md` + `llm-gateway.design.md` + ADR-0009 |
| created_at | 2026-04-04 |
| updated_at | 2026-04-04 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Phase 1 MVP tasks T-LGW-001..T-LGW-011.5 (bounded slices sized for ~10 code and ~10 test files max per sprint wave); Phase 2 hardening tasks T-LGW-012..T-LGW-015.5; Phase 3 acceleration tasks T-LGW-016..T-LGW-018 |
| acceptance_criteria_scope | AC-GW-001..AC-GW-008 mapped to explicit tasks, owners, file scopes, and deterministic commands |
| dependency_order | Phase 1 contract foundation -> phase-1 convergence -> phase-2 hardening -> phase-2 convergence -> phase-3 parity and service seam |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000124-llm-gateway/llm-gateway.plan.md |
| branch | prj0000124-llm-gateway (validated PASS before artifact writes) |
| first_red_slice | RED-SLICE-LGW-001 on `tests/core/gateway/test_gateway_core_orchestration.py` with fail-closed sequence assertions and selector `python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py -k fail_closed` |
| validation_evidence | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 17 passed in 9.00s |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Large split-plane plans stay executable when each task declares owner, explicit file list, AC mapping, and at least one deterministic selector. |
| Root cause | Placeholder plans and vague tasks create downstream ambiguity between @5test, @6code, @7exec, and @8ql gates. |
| Prevention | Enforce mandatory task schema (objective, files, owner, dependencies, validation command, AC mapping) and include explicit convergence steps for parallel-safe waves. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync; prj0000122-jwt-refresh-token-support; prj0000124-llm-gateway |
| Recurrence count | 3 |
| Promotion status | PROMOTED_TO_HARD_RULE |

## prj0000122 - jwt-refresh-token-support

| Field | Value |
|---|---|
| task_id | prj0000122-jwt-refresh-token-support |
| owner_agent | @4plan |
| source | user request + project overview + think artifact + design artifact + ADR-0008 |
| created_at | 2026-04-04 |
| updated_at | 2026-04-04 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Chunk C1 (T-JRT-001..T-JRT-006) for red contracts and bounded backend implementation; Chunk C2 (T-JRT-007..T-JRT-009) for execution, quality, and git closure |
| acceptance_criteria_scope | AC-JRT-001..AC-JRT-009 mapped to IFACE-JRT-001..IFACE-JRT-009 with explicit owners, target files, and validation commands |
| dependency_order | Parallel red wave (T-JRT-001 || T-JRT-002 || T-JRT-003) -> T-JRT-004 -> T-JRT-005 -> T-JRT-006 -> T-JRT-007 -> T-JRT-008 -> T-JRT-009 |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.plan.md |
| branch | prj0000122-jwt-refresh-token-support (validated PASS before artifact writes) |
| first_red_slice | T-JRT-001 only: create `tests/test_backend_refresh_sessions.py` with temp store-path fixture, bootstrap success/401, refresh success, replay 401, and no-plaintext-persistence assertions |
| validation_evidence | git branch --show-current -> prj0000122-jwt-refresh-token-support; c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 17 passed in 6.41s |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Red-wave planning is easier to hand off when parallel-safe test tasks are disjoint by file and merged through one explicit convergence artifact. |
| Root cause | Refresh-token work spans three test surfaces, and without a defined merge point the red phase can drift into overlapping ownership. |
| Prevention | Keep the first red wave file-disjoint, reserve shared artifact edits for one convergence task, and require deterministic selectors per file. |
| First seen | 2026-04-04 |
| Seen in | prj0000122-jwt-refresh-token-support |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

| Field | Value |
|---|---|
| task_id | prj0000104-idea000014-processing |
| owner_agent | @4plan |
| source | @3design |
| created_at | 2026-03-30 |
| updated_at | 2026-03-30 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Single chunk for dependency-authority and parity workflow (T001-T013) |
| acceptance_criteria_scope | AC-001..AC-007 fully mapped to tasks and commands |
| dependency_order | @5test red -> @6code green -> @7exec runtime -> @8ql quality/security -> @9git handoff |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000104-idea000014-processing/idea000014-processing.plan.md |
| branch | prj0000104-idea000014-processing (validated PASS before artifact writes) |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Plan handoff quality improves when AC-to-task mapping and command matrix are explicitly paired with owner phases. |
| Root cause | Placeholder plan content did not provide executable downstream sequencing or gate evidence requirements. |
| Prevention | Enforce mandatory task schema (objective, target files, acceptance criteria, validation command) and explicit red/green/runtime/quality/handoff gates. |
| First seen | 2026-03-28 |
| Seen in | prj0000093-projectmanager-ideas-autosync; prj0000104-idea000014-processing |
| Recurrence count | 2 |
| Promotion status | PROMOTED_TO_HARD_RULE |

## prj0000105 - idea000016-mixin-architecture-base

| Field | Value |
|---|---|
| task_id | prj0000105-idea000016-mixin-architecture-base |
| owner_agent | @4plan |
| source | @3design |
| created_at | 2026-03-30 |
| updated_at | 2026-03-30 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Two chunks: Chunk A (T001-T006), Chunk B (T007-T013) |
| acceptance_criteria_scope | AC-MX-001..AC-MX-009 mapped to tasks, files, and commands |
| dependency_order | @5test red -> @6code green -> @7exec runtime -> @8ql quality/security -> @9git handoff |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.plan.md |
| branch | prj0000105-idea000016-mixin-architecture-base (validated PASS before and after artifact update) |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | Project policy gate evidence must be conclusive; interrupted test runs are not valid closure evidence. |
| Root cause | Initial docs policy gate command execution was interrupted, leaving inconclusive state for required governance evidence. |
| Prevention | Re-run the exact required selector immediately and record only conclusive pass/fail output in the artifact. |
| First seen | 2026-03-30 |
| Seen in | prj0000105-idea000016-mixin-architecture-base |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

## prj0000106 - idea000080-smart-prompt-routing-system

| Field | Value |
|---|---|
| task_id | prj0000106-idea000080-smart-prompt-routing-system |
| owner_agent | @4plan |
| source | @3design |
| created_at | 2026-03-30 |
| updated_at | 2026-03-30 |
| status | DONE |
| lifecycle | OPEN -> IN_PROGRESS -> DONE |
| chunk_boundaries | Two chunks: Chunk A guardrail-first routing core (T-SPR-001..T-SPR-013), Chunk B ambiguity/fallback/telemetry (T-SPR-014..T-SPR-021) |
| acceptance_criteria_scope | AC-SPR-001..AC-SPR-008 fully mapped to executable tasks and validation commands |
| dependency_order | @5test red -> @6code green -> @7exec runtime -> @8ql quality/security -> @9git handoff |
| handoff_target | @5test |
| artifact_paths | docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.plan.md |
| branch | prj0000106-idea000080-smart-prompt-routing-system (validated PASS before artifact writes) |
| validation_evidence | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 12 passed in 1.59s |

### Lesson Entry

| Field | Value |
|---|---|
| Pattern | AC-to-task mapping quality improves when each task embeds explicit owner handoff and executable command selectors. |
| Root cause | Placeholder plans without command-level selectors create ambiguity between @5test and @6code ownership boundaries. |
| Prevention | Require per-task owner sequencing in plan phases and include deterministic command selectors per AC mapping. |
| First seen | 2026-03-30 |
| Seen in | prj0000106-idea000080-smart-prompt-routing-system |
| Recurrence count | 1 |
| Promotion status | CANDIDATE |

