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

## prj0000076 - future-ideas-kanban

| Field | Value |
|---|---|
| **task_id** | prj0000076-future-ideas-kanban |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-25 |
| **updated_at** | 2026-03-25 |
| **status** | HANDED_OFF |
| **summary** | prj0000076 future-ideas-kanban branch prj0000076-future-ideas-kanban — project setup complete 2026-03-25 |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000076/prj0000076.project.md, docs/project/kanban.md |

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

---

prj0000073 api-documentation branch prj0000073-api-documentation — project setup complete 2026-03-25

## prj0000074 - workspace-meta-improvements

| Field | Value |
|---|---|
| **task_id** | prj0000074-workspace-meta-improvements |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-25 |
| **updated_at** | 2026-03-25 |
| **status** | HANDED_OFF |
| **summary** | prj0000074 workspace-meta-improvements branch prj0000074-workspace-meta-improvements — project setup complete 2026-03-25 |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000074/prj0000074.project.md |

---

prj0000075 ci-simplification branch prj0000075-ci-simplification — project setup complete 2026-03-25

## prj0000081 - mcp-server-ecosystem

| Field | Value |
|---|---|
| **task_id** | prj0000081-mcp-server-ecosystem |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-26 |
| **updated_at** | 2026-03-26 |
| **status** | HANDED_OFF |
| **summary** | prj0000081 mcp-server-ecosystem branch prj0000081-mcp-server-ecosystem — project folder created, all 9 stubs initialised, scope boundary `src/mcp/` chosen (first-class subsystem, not tool plugin), handed off to @2think for deep analysis of MCP community registries, PyAgent tool-dispatch integration, security threat model, and 3+ implementation approaches. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.project.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.think.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.design.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.plan.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.test.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.code.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.exec.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.ql.md, docs/project/prj0000081-mcp-server-ecosystem/mcp-server-ecosystem.git.md |

---

## prj0000085 - shadow-mode-replay

| Field | Value |
|---|---|
| **task_id** | prj0000085-shadow-mode-replay |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | prj0000085 shadow-mode-replay branch prj0000085-shadow-mode-replay - project folder created with overview and 8 lifecycle stubs; branch gate validated; structure tests run. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.project.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.think.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.design.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.plan.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.test.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.code.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.exec.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.ql.md, docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.git.md |

