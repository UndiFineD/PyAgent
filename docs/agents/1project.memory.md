# 1project Memory

## prj001 - conftest-typing-fixes

| Field | Value |
|---|---|
| **task_id** | prj001-conftest-typing-fixes |
| **owner_agent** | @1project |
| **source** | @1project |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Hardened static typing in conftest.py: replaced cast(_SessionWithExitStatus, session).exitstatus = 1 with direct session.exitstatus = 1; tightened Protocols; removed stale type: ignore comments; fixed WriteTracker.logged_open return type. |
| **handoff_target** | @7exec |
| **artifact_paths** | conftest.py, tests/test_conftest.py, docs/project/prj001-conftest-typing-fixes/ |

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @1project |
| **source** | @1project |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | IN_PROGRESS |
| **summary** | Extend agent workflow so each agent writes incremental checkpoints after every finding, not just at completion. Adds per-project artifact files for @5test–@9git (test.md, code.md, exec.md, ql.md, git.md) and updates agent mode instructions with a checkpoint cadence policy. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/ |

---

## prj0000045 - transaction-managers-full

| Field | Value |
|---|---|
| **task_id** | prj0000045-transaction-managers-full |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-22 |
| **updated_at** | 2026-03-22 |
| **status** | HANDED_OFF |
| **summary** | Set up project folder docs/project/prj0000045/. Created all 9 stub files. @2think analysis complete (2think.memory.md §3.1 + §3.3, Option B binding). M1–M4 DONE for original scope. Scope extended 2026-03-22: ContextWindow added (src/context_manager/ContextWindow.py + src/context_manager/__init__.py + tests/test_ContextWindow.py). @4plan must add T15; @5test must add test_ContextWindow.py; @6code implements T00–T15. Branch `prj0000045-transaction-managers-full` confirmed active. |
| **handoff_target** | @4plan (T15 ContextWindow addition) → @5test → @6code |
| **artifact_paths** | docs/project/prj0000045/, src/transactions/ (to be created), src/context_manager/ContextWindow.py (to be created), src/core/ProcessTransactionManager.py (to be created), src/core/ContextTransactionManager.py (to be created) |
