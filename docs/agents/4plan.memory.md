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
