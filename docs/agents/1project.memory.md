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
