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

---

## prj0000087 - n8n-workflow-bridge

| Field | Value |
|---|---|
| **task_id** | prj0000087-n8n-workflow-bridge |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | prj0000087 n8n-workflow-bridge branch prj0000087-n8n-workflow-bridge - project folder created with overview and 8 lifecycle stubs; branch gate validated; structure tests run. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.project.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.design.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.plan.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.test.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.code.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.exec.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.ql.md, docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.git.md |

---

## prj0000089 - agent-learning-loop

| Field | Value |
|---|---|
| **task_id** | prj0000089-agent-learning-loop |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | HANDED_OFF |
| **summary** | Project boundary initialized on branch prj0000089-agent-learning-loop. Created canonical project overview plus think/design/plan and downstream lifecycle stubs. Registered project in Discovery lane and project registry; advanced nextproject to prj0000090. Ready for @2think options exploration focused on reducing recurring agent mistakes via .github/agents guidance and process docs. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000089-agent-learning-loop/agent-learning-loop.project.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.think.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.design.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.plan.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.test.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.code.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.exec.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.ql.md, docs/project/prj0000089-agent-learning-loop/agent-learning-loop.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

---

## prj0000090 - private-key-remediation

| Field | Value |
|---|---|
| **task_id** | prj0000090-private-key-remediation |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **summary** | Project boundary initialized on expected branch prj0000090-private-key-remediation from idea000001-private-key-in-repo. Created canonical overview plus think/design/plan and downstream lifecycle stubs; registered project in Discovery lane and advanced nextproject to prj0000091. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.project.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.think.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.design.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.plan.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.test.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.code.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.exec.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.ql.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

---

## prj0000091 - missing-compose-dockerfile

| Field | Value |
|---|---|
| **task_id** | prj0000091-missing-compose-dockerfile |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **summary** | Project boundary initialized on expected branch prj0000091-missing-compose-dockerfile from idea000002-missing-compose-dockerfile. Created canonical overview plus think/design/plan and downstream lifecycle stubs; registered project in Discovery lane and advanced nextproject to prj0000092. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.project.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.plan.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.test.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.code.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.exec.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.ql.md, docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

---

## prj0000092 - mypy-strict-enforcement

| Field | Value |
|---|---|
| **task_id** | prj0000092-mypy-strict-enforcement |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **summary** | Project boundary initialized on expected branch prj0000092-mypy-strict-enforcement from idea000003-mypy-strict-enforcement. Created canonical overview plus think/design/plan and downstream lifecycle stubs; registered project in Discovery lane and advanced nextproject to prj0000093. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.project.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.design.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.plan.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.test.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.code.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.exec.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.ql.md, docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

---

## prj0000093 - projectmanager-ideas-autosync

| Field | Value |
|---|---|
| **task_id** | prj0000093-projectmanager-ideas-autosync |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **summary** | Project boundary initialized on expected branch prj0000093-projectmanager-ideas-autosync. Created canonical overview plus think/design/plan and downstream lifecycle stubs; registered project in Discovery lane and advanced nextproject to prj0000094. Scope includes backend ideas API + frontend Project Manager integration + tests. |
| **handoff_target** | @2think |
| **artifact_paths** | docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.think.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.design.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.plan.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.test.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.code.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.exec.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.ql.md, docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

---

## prj0000095 - source-stub-remediation

| Field | Value |
|---|---|
| **task_id** | prj0000095-source-stub-remediation |
| **owner_agent** | @1project |
| **source** | @0master |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **summary** | Project governance wrap-up completed on branch prj0000095-source-stub-remediation: kanban moved from Discovery to Review, project overview refreshed to implementation-complete handoff state, and git summary marked READY_FOR_9GIT with scoped change notes. |
| **handoff_target** | @9git |
| **artifact_paths** | docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.project.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.think.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.design.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.test.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.code.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.exec.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.ql.md, docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.git.md, docs/project/kanban.md, data/projects.json, data/nextproject.md |

