# 3design Memory

This file records finalized design decisions, 
architecture diagrams, and key interface contracts.

## Auto-handoff (Design → Plan)

Once a design is finalized, the next agent in the workflow is **@4plan**.  
The designer agent should invoke **@4plan** via `agent/runSubagent` 
so the planning work is started automatically 
and the work is correctly attributed.

When calling `agent/runSubagent`, include a clear task description 
and any relevant context/links to the design decisions 
so the planning agent can continue without having to re-derive 
the design intent.

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Designed checkpoint rule (Step-Gated Full Overwrite) for all 9 agent artifact files. Templates inline per agent. @1project pre-creates all 9 stubs. Checkpoint rule applies to all artifact types. Documents updated before next runSubagent call. |

---

## prj0000052 - project-management

| Field | Value |
|---|---|
| **task_id** | prj0000052-project-management |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-24 |
| **updated_at** | 2026-03-24 |
| **status** | DONE |
| **branch** | prj0000052-project-management |
| **artifact** | docs/project/prj0000052/project-management.design.md |
| **selected_option** | Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop) |
| **summary** | Full design for 6 deliverables: (1) docs/project/kanban.md with all 62 projects in 7 lanes; (2) data/projects.json with complete 62-entry array; (3) web/apps/ProjectManager.tsx React Kanban component; (4) backend/app.py GET /api/projects endpoint + ProjectModel; (5) 0master.agent.md + 1project.agent.md additions; (6) web/App.tsx + web/types.ts registration. Status: DONE — report back to @0master (no @4plan handoff). |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/agent-doc-frequency.design.md |
---

## prj0000045 - transaction-managers-full

| Field | Value |
|---|---|
| **task_id** | prj0000045-transaction-managers-full |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-22 |
| **updated_at** | 2026-03-22 |
| **status** | HANDED_OFF |
| **branch_gate** | WARN — designed on `main`; expected `prj0000045-transaction-managers-full` |
| **selected_option** | Option B — `src/transactions/` package with BaseTransaction ABC |
| **key_decisions** | Dual-API coexistence (single class, two constructor modes); Fernet encryption (cryptography pkg, HKDF per-user key, user_id=None skips); httpx remote sync with dry_run=True for tests; ContextTransaction UUID lineage auto-wired from contextvar stack; ContextWindow LLM handoff deferred to follow-on project |
| **interface_contracts** | See design.md §Interfaces & Contracts; 5 open questions documented for @4plan |
| **shim_strategy** | 3 new src/core/ shims + 1 replacement src/MemoryTransactionManager.py shim |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000045/transaction-managers-full.design.md |

---

## prj0000047 - conky-real-metrics

| Field | Value |
|---|---|
| **task_id** | prj0000047-conky-real-metrics |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-23 |
| **updated_at** | 2026-03-23 |
| **status** | DONE |
| **branch_gate** | PASS — `prj0000047-conky-real-metrics` |
| **selected_option** | Option A — REST Polling `GET /api/metrics/system` (psutil, module-level delta state) |
| **key_decisions** | 2s poll interval; `useSystemMetrics(2000)` custom hook; stay-on-last-values error strategy + OFFLINE badge; no Vite dev plugin needed (existing /api proxy sufficient); memory surfaces used_mb/total_mb/percent; disk I/O row added to UI; interface filter by name prefix (lo, docker, veth, br-, virbr, tun, tap, loopback, isatap, teredo) |
| **interface_contracts** | `SystemMetrics` TS interface; `SystemMetricsResponse` Pydantic model; `useSystemMetrics` hook; `_is_physical_iface()` helper; module-level `_prev_net` + `_prev_disk` delta state |
| **vite_config_change** | None required |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000047/conky-real-metrics.design.md |

---

## prj0000086 - universal-agent-shell

| Field | Value |
|---|---|
| **task_id** | prj0000086-universal-agent-shell |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **branch_gate** | PASS — `prj0000086-universal-agent-shell` |
| **selected_option** | Option B — Universal Shell Facade with Controlled Legacy Fallback |
| **design_path** | Minimal facade module under `src/core/universal/` with `UniversalIntentRouter.py`, `UniversalCoreRegistry.py`, `UniversalAgentShell.py`, `exceptions.py`, `__init__.py` |
| **interface_contracts** | `TaskEnvelope`, `RoutingDecision`, `DispatchResult`, async `CoreHandler.execute(envelope)`, one-shot fallback policy |
| **assumptions** | Allowlist-gated core routing, single fallback attempt, deterministic normalization, constructor-injected dependencies |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md |

---

## prj0000088 - ai-fuzzing-security

| Field | Value |
|---|---|
| **task_id** | prj0000088-ai-fuzzing-security |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **branch_gate** | PASS - `prj0000088-ai-fuzzing-security` |
| **selected_option** | Option A - Deterministic Local Mutation Engine |
| **design_path** | `src/core/fuzzing/` contracts for `FuzzCase`, `FuzzMutator`, `FuzzCorpus`, `FuzzEngineCore`, `FuzzSafetyPolicy`, `FuzzResult`, `exceptions`, and `__init__` |
| **interface_contracts** | Deterministic replay key, mutation operator protocol, policy limits, campaign run/build/execute API, typed result aggregation and exception hierarchy |
| **assumptions** | Local-only targets, allowlist enforcement, no external network paths, seed-based deterministic scheduling |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.design.md |
